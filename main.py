from chat import Chatter



if __name__ == "__main__":
    chatter = Chatter()

    # print(chatter._get_prompt_with_rag('我国半导体发展前景如何', url_topk=5, chunk_topk=3))


    # reply, messages = chatter.chat_with_rag('我国半导体发展前景如何')
    # print(reply)
    # print('\n\n##############\n\n')
    # reply, messages = chatter.chat_no_rag('建议什么时候购买半导体基金', messages=messages)
    # print(reply)


    reply, messages = chatter.chat_no_rag('我国半导体发展前景如何')
    print(reply)
    print('\n\n##############\n\n')
    reply, messages = chatter.chat_no_rag('建议什么时候购买半导体基金', messages=messages)
    print(reply)