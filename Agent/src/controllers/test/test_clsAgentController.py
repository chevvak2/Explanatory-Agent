import unittest
import json
import os
from modApp import app
import requests_mock
from controllers.clsAgentController import knowledgeProviderUrl


class test_clsAgentController(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        self.app = None

    @staticmethod
    def loadJsonFromFile(fileName):
        fullPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), fileName)
        with open(fullPath) as file:
            return json.load(file)

    def test_user_request_body_works_with_json_header(self):
        userRequestBody = json.dumps(self.loadJsonFromFile("test_user_request_body_nominal.json"))
        knowledgeProviderResponseBody = json.dumps(self.loadJsonFromFile("test_knowledge_provider_response_body_nominal.json"))
        agentResponseBody = self.loadJsonFromFile("test_agent_response_body_nominal.json")
        with requests_mock.Mocker() as mocker:
            mocker.register_uri('POST', knowledgeProviderUrl, text=knowledgeProviderResponseBody)
            response = self.app.post('/agent', headers={"Content-Type": "application/json"}, data=userRequestBody, follow_redirects=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual(agentResponseBody, response.json)

    def test_user_request_body_works_with_text_header(self):
        userRequestBody = json.dumps(self.loadJsonFromFile("test_user_request_body_nominal.json"))
        knowledgeProviderResponseBody = json.dumps(self.loadJsonFromFile("test_knowledge_provider_response_body_nominal.json"))
        agentResponseBody = self.loadJsonFromFile("test_agent_response_body_nominal.json")
        with requests_mock.Mocker() as mocker:
            mocker.register_uri('POST', knowledgeProviderUrl, text=knowledgeProviderResponseBody)
            response = self.app.post('/agent', headers={"Content-Type": "text/json"}, data=userRequestBody, follow_redirects=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual(agentResponseBody, response.json)

    def test_user_request_body_works_without_header(self):
        userRequestBody = json.dumps(self.loadJsonFromFile("test_user_request_body_nominal.json"))
        knowledgeProviderResponseBody = json.dumps(self.loadJsonFromFile("test_knowledge_provider_response_body_nominal.json"))
        agentResponseBody = self.loadJsonFromFile("test_agent_response_body_nominal.json")
        with requests_mock.Mocker() as mocker:
            mocker.register_uri('POST', knowledgeProviderUrl, text=knowledgeProviderResponseBody)
            response = self.app.post('/agent', data=userRequestBody, follow_redirects=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual(agentResponseBody, response.json)

    def test_user_request_body_bad_request(self):
        userRequestBody = 'garbage'
        knowledgeProviderResponseBody = 'also garbage'
        agentResponseBody = {"message": "Supplied request body does not conform"}
        with requests_mock.Mocker() as mocker:
            mocker.register_uri('POST', knowledgeProviderUrl, text=knowledgeProviderResponseBody)
            response = self.app.post('/agent', data=userRequestBody, follow_redirects=True)
        self.assertEqual(400, response.status_code)
        self.assertEqual(agentResponseBody, response.json)

    def test_knowlegdge_provider_response_body_unknown_internal_server_error(self):
        userRequestBody = json.dumps(self.loadJsonFromFile("test_user_request_body_nominal.json"))
        knowledgeProviderResponseBody = "garbage"
        agentResponseBody = {"message": "Knowledge Provider response body does not conform, have they changed their API?"}
        with requests_mock.Mocker() as mocker:
            mocker.register_uri('POST', knowledgeProviderUrl, text=knowledgeProviderResponseBody)
            response = self.app.post('/agent', headers={"Content-Type": "application/json"}, data=userRequestBody, follow_redirects=True)
        self.assertEqual(500, response.status_code)
        self.assertEqual(agentResponseBody, response.json)


if __name__ == '__main__':
    unittest.main()
