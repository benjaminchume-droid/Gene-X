from gene.execution.terminal import Terminal
def test_terminal_executes_real_process():
    result=Terminal().run(["python","-c","print('ok')"])
    assert result.returncode==0 and "ok" in result.stdout
