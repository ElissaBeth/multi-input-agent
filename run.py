import os, time

if __name__ == '__main__': # required for Windows

    db_folder = 'data'
    os.makedirs(db_folder, exist_ok=True)

    agents = {}

    from agent_news import AgentNews

    sys_prompt = "You are a news synopsys posting bot named agent-news. " \
    "Don't talk about yourself, just post the news!"
    agents["agent-news"] = AgentNews("agent-news", sys_prompt, db_folder, 200, 200)


    for agent in agents.values(): agent.start()

    # wait for all agents to be ready
    while any(not agent.ready for agent in agents.values()):
        try: time.sleep(0.1)
        except KeyboardInterrupt:
            for agent in agents.values(): agent.proc_ctrl.value = 0
        for agent in agents.values(): agent.print_status()
    print(f"{__name__:<26} all agents ready")

    while all(agent.running for agent in agents.values()):
        deadline = time.time() + 10.0
        while all(agent.running for agent in agents.values()) and time.time() < deadline:
            try: time.sleep(0.1)
            except KeyboardInterrupt:
                for agent in agents.values(): agent.proc_ctrl.value = 0
            for agent in agents.values(): agent.print_status()
        print(f"{__name__:<26} ping")

    print('STOPPING')
    for agent in agents.values(): agent.stop()
