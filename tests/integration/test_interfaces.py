from interfaces.cli import CliApp
from interfaces.protocols import Response
class H:
    def handle(self,request): return Response(True,request.operation)
def test_cli_boundary(): assert CliApp(H()).dispatch("probe").payload=="probe"
