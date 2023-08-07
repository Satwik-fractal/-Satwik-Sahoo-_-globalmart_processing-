import requests

api_endpoint = "https://zucwflxqsxrsmwseehqvjmnx2u0cdigp.lambda-url.ap-south-1.on.aws/mentorskool/v1/sales"

response = requests.get(api_endpoint,headers={"access_token":"fe66583bfe5185048c66571293e0d358"})
print("Content:", response.text)
