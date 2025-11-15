from zork_ai import manager, alias, client
# Set the model to use and generate a streaming response
stream = client.responses.create(
    model=manager.get_model_info(alias).id,
    input="What is the answer to the ultimate question of life, the universe and everything?",
    stream=True
)

# Print the streaming response
for chunk in stream:
    # For Responses API, the structure is different
    # Check if there's content in the chunk
    print(chunk)