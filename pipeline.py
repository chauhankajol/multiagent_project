from agents import build_search_agent,build_read_agent,writer_chain,critic_chain

def run_research_pipeline(topic:str) -> dict :

    state={}
    #search agent working
    print("\n"+" ="*50)
    print("step 1 - search agent is working...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages":[("user", f"recent reliable and detailed information about the:{topic}")]
    })
    state["search_result"]=search_result['messages'][-1].content
    print("\n search result",state['search_result'])


    #step-2  reader agent
    print("/n"+' ='*50)
    print("step-2  reader agent scraping the top resources...")
    print("="*50)

    reader_agent = build_read_agent()
    reader_result = reader_agent.invoke({ 
    "messages": [
        (
            "user",
            f"""
Based on the following search results about '{topic}',
pick the relevant URL and scrape it for relevant content.

Search results:

{state['search_result'][:300]}
"""
        )
    ]
})
    state["scraped_content"] = reader_result["messages"][-1].content
    print("\n"+" ="*50)
    print("step-3 writer draft the  report")
    print("="*50)

    research_combined =(
        f"search_result:\n{state['search_result']}\n\n"
        f"scraped_content:\n{state['scraped_content']}"
    )

    state['report']=writer_chain.invoke({
        "topic":topic,
        "research":research_combined 
    })
    print("/n Final Report\n",state['report'])


    #critic report 
    print("/n"+" ="*50)
    print("step-4 critic is reviewing the report")
    print("="*50)

    state["feedback"]= critic_chain.invoke({
        "report":state['report']
    })

    print("\n critic report \n ",state["feedback"])

    return state

if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)
