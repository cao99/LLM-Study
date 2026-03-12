from mcp.server.fastmcp import FastMCP
from kubernetes import client, config
import os
import sys

# ==============================================================================
# 1. 实例化 K8s 监控专用大脑
# ==============================================================================
mcp = FastMCP("K8s-Monitor-Expert")

# ==============================================================================
# 2. 注册 K8s Pod 查询工具
# LLM 看到这个工具时，会根据 docstring 提示用户输入参数。
# ==============================================================================
@mcp.tool()
def list_pods(namespace: str = "default") -> str:
    """列出指定 Kubernetes 命名空间下的所有 Pod 及其核心运维信息。
    
    Args:
        namespace: 命名空间名称 (默认为 "default")
    """
    # .strip()：这是 Python 字符串对象自带的方法，作用是去掉字符串首尾的空格、换行符（\n）、制表符（\t）等不可见字符。
    namespace = namespace.strip()
    
    try: #try是 Python 的异常处理机制的开头。意思是"尝试执行以下代码，如果出错了别崩溃，走到后面的 except 里处理"
        # 加载本地的 kubeconfig
        config.load_kube_config()
        
        # 调试日志：确认当前正在使用的 Context (输出到 stderr)
        _, active_context = config.list_kube_config_contexts()
        print(f"[后端日志] 正在使用的 K8s Context: {active_context['name']}", file=sys.stderr)
        print(f"[后端日志] 正在查询 Namespace: '{namespace}'", file=sys.stderr)

        v1 = client.CoreV1Api()
        
        # 调用 K8s API 获取 Pod 列表
        pods = v1.list_namespaced_pod(namespace)
        
        if not pods.items:
            return f"在命名空间 '{namespace}' 中没有发现任何 Pod。"
        
        # 格式化输出，只保留关键运维指标
        output = [f"命名空间 '{namespace}' 中的 Pod 列表如下：\n"]
        output.append(f"{'NAME':<40} {'STATUS':<15} {'RESTARTS':<10} {'IP':<15}")
        output.append("-" * 80)
        
        for pod in pods.items:
            name = pod.metadata.name
            status = pod.status.phase
            # 获取所有容器的总重启次数
            restarts = sum(c.restart_count for c in pod.status.container_statuses) if pod.status.container_statuses else 0
            pod_ip = pod.status.pod_ip or "None"
            
            output.append(f"{name:<40} {status:<15} {restarts:<10} {pod_ip:<15}")
            
        return "\n".join(output)

    except Exception as e:
        return f"查询出错：{str(e)}"

@mcp.tool()
def describe_pod(pod_name: str, namespace: str = "default") -> str:
    """获取指定 Pod 的详细信息，包括状态、容器信息以及最近的事件日志。
    
    Args:
        pod_name: Pod 的准确名称
        namespace: 命名空间 (默认为 "default")
    """
    pod_name = pod_name.strip()
    namespace = namespace.strip()
    
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        
        # 1. 获取 Pod 核心对象
        pod = v1.read_namespaced_pod(pod_name, namespace)
        
        # 2. 获取 Pod 相关事件 (Events)
        events = v1.list_namespaced_event(namespace, field_selector=f"involvedObject.name={pod_name}")
        
        res = [f"=== Pod 详情: {pod_name} (NS: {namespace}) ==="]
        res.append(f"状态: {pod.status.phase}")
        res.append(f"节点: {pod.spec.node_name}")
        res.append(f"镜像: {[c.image for c in pod.spec.containers]}")
        
        res.append("\n--- 最近事件 (Events) ---")
        if not events.items:
            res.append("没有发现相关的异常事件。")
        else:
            for e in sorted(events.items, key=lambda x: x.last_timestamp or x.event_time or "", reverse=True)[:5]:
                t = e.last_timestamp or e.event_time
                res.append(f"[{t}] {e.type}: {e.reason} - {e.message}")
        
        return "\n".join(res)
    except Exception as e:
        return f"获取详情失败: {str(e)}"

@mcp.tool()
def get_pod_logs(pod_name: str, namespace: str = "default", tail_lines: int = 100) -> str:
    """获取指定 Pod 的容器日志，用于定位程序内部错误。
    
    Args:
        pod_name: Pod 名称
        namespace: 命名空间 (默认为 "default")
        tail_lines: 返回最后的行数 (默认为 100)
    """
    pod_name = pod_name.strip()
    namespace = namespace.strip()
    
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        
        # 获取日志
        logs = v1.read_namespaced_pod_log(
            name=pod_name, 
            namespace=namespace, 
            tail_lines=tail_lines
        )
        
        if not logs:
            return f"Pod '{pod_name}' 目前没有输出任何日志。"
            
        return f"=== Pod 日志 (最后 {tail_lines} 行) ===\n{logs}"
    except Exception as e:
        return f"获取日志失败: {str(e)}"

@mcp.tool()
def delete_pod(pod_name: str, namespace: str = "default") -> str:
    """删除指定的 Pod。通常用于强制触发 Deployment 重新调度。
    
    Args:
        pod_name: 要删除的 Pod 名称
        namespace: 命名空间 (默认为 "default")
    """
    pod_name = pod_name.strip()
    namespace = namespace.strip()
    
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        
        v1.delete_namespaced_pod(name=pod_name, namespace=namespace)
        
        return f"✅ 成功发起删除指令：Pod '{pod_name}' 正在被清理。"
    except Exception as e:
        return f"删除失败: {str(e)}"

# ==============================================================================
# 3. 运行 MCP 服务
# ==============================================================================
if __name__ == "__main__":
    mcp.run()
