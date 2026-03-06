class GmpSyncAgentsTestMixin:
    def test_sync_agents(self):
        self.gmp.sync_agents()

        self.connection.send.has_been_called_with(b"<sync_agents/>")
