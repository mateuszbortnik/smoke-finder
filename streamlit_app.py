import client
from client import RestClient
client = RestClient("marketing@mta.digital", "92626ed1261a7edf")

post_data = dict()
# simple way to set a task
post_data[len(post_data)] = dict(
    domain="www.ashleystewart.com"
)
# after a task is completed, we will send a GET request to the address you specify
# instead of $id and $tag, you will receive actual values that are relevant to this task
post_data[len(post_data)] = dict(
    domain="www.ashleystewart.com",
    depth=100,
    # priority=2,
    # tag="some_string_123",
    pingback_url="https://your-server.com/pingscript?id=$id&tag=$tag"
)
# after a task is completed, we will send a GET request to the address you specify
# instead of $id and $tag, you will receive actual values that are relevant to this task
post_data[len(post_data)] = dict(
    domain="www.ashleystewart.com",
    postback_url="https://your-server.com/postbackscript"
)
# POST /v3/business_data/trustpilot/reviews/task_post
response = client.post("/v3/business_data/trustpilot/reviews/task_post", post_data)
# you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
if response["status_code"] == 20000:
    print(response)
    # do something with result
else:
    print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))

st.write(response)