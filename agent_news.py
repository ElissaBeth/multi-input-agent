import multiprocessing as mp

class AgentNews:
    def __init__(self, name, sys_prompt, db_folder, ctx_queue_max, gen_queue_max):
        self.name, self.sys_prompt, self.db_folder = name, sys_prompt, db_folder

        self.proc_ctrl   = mp.Value('b', 1)
        self.proc_status = mp.Queue()
        self.proc_stop   = mp.Event()
        self.queues = {}
        self.queues['ctx'] = mp.Queue(maxsize=ctx_queue_max)
        self.queues['gen'] = mp.Queue(maxsize=gen_queue_max)
        self.procs = {}

    def start(self):
        queue_ctx = self.queues['ctx']
        queue_gen = self.queues['gen']

        from tools.write_rnd_synopsys import WriteRndSynopsys
        obj = WriteRndSynopsys(self.db_folder)
        name = 'write_rnd_synopsys'; self.procs[name] = []
        self.procs[name].append(mp.Process(target=obj.load_proc, name=f"{self.name}_{name}_00", args=(self.proc_ctrl, self.proc_status, self.proc_stop, queue_ctx)))

        from tools.post_discord_wh import PostDiscordWH
        obj = PostDiscordWH(self.db_folder, self.name)
        name = 'post_discord_wh'; self.procs[name] = []
        self.procs[name].append(mp.Process(target=obj.load_proc, name=f"{self.name}_{name}_00", args=(self.proc_ctrl, self.proc_status, self.proc_stop, queue_gen)))


        from model_ollama_one import ModelSingle
        obj_model = ModelSingle(self.db_folder, self.sys_prompt)
        self.procs['model'] = [mp.Process(target=obj_model.load_proc, name=self.name+'_model', args=(self.proc_ctrl, self.proc_status, self.proc_stop, queue_ctx, queue_gen))]

        for procs in self.procs.values():
            for proc in procs: proc.start()

    def stop(self):
        self.proc_ctrl.value = 0
        self.proc_stop.set()
        for queue in self.queues.values():
            if not queue.empty(): queue.get_nowait()
        for procs in self.procs.values():
            for proc in procs: proc.join()

    def print_status(self):
        while not self.proc_status.empty(): print(f"{self.name:<7} " + self.proc_status.get_nowait())

    @property
    def ready(self):
        total = sum(len(procs) for procs in self.procs.values())
        return self.proc_ctrl.value > total

    @property
    def running(self):
        return self.proc_ctrl.value != 0
