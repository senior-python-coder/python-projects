import tkinter as tk
from tkinter import ttk
import math


class TowerOfHanoiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tower of Hanoi - PyCharm")
        self.width = 700
        self.height = 400
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="#f7f7f7")
        self.canvas.grid(row=0, column=0, columnspan=6, padx=10, pady=10)

        # Controls
        tk.Label(root, text="Disks:").grid(row=1, column=0, sticky="w")
        self.disks_var = tk.IntVar(value=4)
        self.disks_spin = tk.Spinbox(root, from_=1, to=8, width=4, textvariable=self.disks_var)
        self.disks_spin.grid(row=1, column=1, sticky="w")

        self.start_btn = ttk.Button(root, text="Start (Generate)", command=self.setup)
        self.start_btn.grid(row=1, column=2)

        self.step_btn = ttk.Button(root, text="Step", command=self.step)
        self.step_btn.grid(row=1, column=3)

        self.auto_btn = ttk.Button(root, text="Auto Play", command=self.toggle_auto)
        self.auto_btn.grid(row=1, column=4)

        self.reset_btn = ttk.Button(root, text="Reset", command=self.reset)
        self.reset_btn.grid(row=1, column=5)

        tk.Label(root, text="Speed (ms):").grid(row=2, column=0, sticky="w")
        self.speed_var = tk.IntVar(value=300)
        self.speed_scale = tk.Scale(root, from_=50, to=1000, orient=tk.HORIZONTAL, variable=self.speed_var)
        self.speed_scale.grid(row=2, column=1, columnspan=2, sticky="we")

        self.status_label = tk.Label(root, text="Move: 0 / 0")
        self.status_label.grid(row=2, column=3, columnspan=3)

        # Peg positions
        self.pegs_x = [self.width * 0.2, self.width * 0.5, self.width * 0.8]
        self.ground_y = self.height * 0.75
        self.peg_height = 150
        self.peg_width = 10

        # Animation & state
        self.disks = []  # list of disk ids
        self.pegs = [[], [], []]  # each peg: stack of disk indices (0 = smallest)
        self.n = 4
        self.moves = []  # list of moves tuples (from, to)
        self.move_index = 0
        self.is_animating = False
        self.auto_play = False

        self.draw_scene()
        self.setup()

    def draw_scene(self):
        self.canvas.delete("all")
        # draw ground
        self.canvas.create_rectangle(0, self.ground_y, self.width, self.height, fill="#e0e0e0", outline="")
        # draw pegs
        for x in self.pegs_x:
            self.canvas.create_rectangle(x - self.peg_width/2, self.ground_y - self.peg_height,
                                         x + self.peg_width/2, self.ground_y, fill="#5c5c5c")

    def setup(self):
        if self.is_animating:
            return
        self.n = max(1, min(8, int(self.disks_var.get())))
        self.moves = []
        self.move_index = 0
        self.pegs = [list(range(self.n-1, -1, -1)), [], []]  # store disk indices with 0 smallest
        self.generate_moves(self.n, 0, 2, 1)
        self.draw_scene()
        self.create_disks()
        self.update_status()

    def reset(self):
        if self.is_animating:
            return
        self.auto_play = False
        self.move_index = 0
        self.pegs = [list(range(self.n-1, -1, -1)), [], []]
        self.draw_scene()
        self.create_disks()
        self.update_status()

    def generate_moves(self, n, frm, to, aux):
        # recursive generation
        if n == 0:
            return
        self.generate_moves(n-1, frm, aux, to)
        self.moves.append((frm, to))
        self.generate_moves(n-1, aux, to, frm)

    def create_disks(self):
        # remove old disks
        for d in self.disks:
            try:
                self.canvas.delete(d)
            except Exception:
                pass
        self.disks = []

        disk_height = 20
        max_width = 140
        min_width = 40
        width_step = 0
        if self.n > 1:
            width_step = (max_width - min_width) / (self.n - 1)

        for i in range(self.n):
            disk_width = max_width - i * width_step
            x = self.pegs_x[0]
            y = self.ground_y - disk_height * (len(self.pegs[0]) - self.pegs[0].index(i)) - 5
            left = x - disk_width/2
            right = x + disk_width/2
            color = self.disk_color(i)
            rect = self.canvas.create_rectangle(left, y - disk_height, right, y, fill=color, outline="#333")
            text = self.canvas.create_text(x, y - disk_height/2, text=str(self.n - i), fill="white")
            # group rectangle and text as a single object by using a tag
            tag = f"disk_{i}"
            self.canvas.addtag_withtag(tag, rect)
            self.canvas.addtag_withtag(tag, text)
            self.disks.append(tag)

        # reposition properly according to pegs stacks
        self.reposition_all()

    def disk_color(self, i):
        # generate a simple color gradient
        hue = int(255 - (i * 200 / max(1, self.n-1)))
        r = (hue * 3) % 256
        g = (hue * 5) % 256
        b = (hue * 7) % 256
        return f"#{r:02x}{g:02x}{b:02x}"

    def reposition_all(self):
        # place each disk according to its peg and stack height
        disk_height = 20
        for peg_index in range(3):
            stack = list(self.pegs[peg_index])[:]  # copy
            for level, disk_id in enumerate(reversed(stack)):
                tag = f"disk_{disk_id}"
                x = self.pegs_x[peg_index]
                y = self.ground_y - disk_height * (level + 1) - 5
                self.move_disk_to_tag(tag, x, y, instant=True)

    def move_disk_to_tag(self, tag, x, y, instant=False):
        # move both rectangle and text that share the tag center to (x, y)
        bbox = self.canvas.bbox(tag)
        if bbox is None:
            return
        cx = (bbox[0] + bbox[2]) / 2
        cy = (bbox[1] + bbox[3]) / 2
        dx = x - cx
        dy = y - cy
        if instant or self.speed_var.get() <= 0:
            self.canvas.move(tag, dx, dy)
        else:
            steps = max(1, int(self.speed_var.get() / 25))
            step_dx = dx / steps
            step_dy = dy / steps
            self.animate_move(tag, step_dx, step_dy, steps)

    def animate_move(self, tag, step_dx, step_dy, steps):
        if steps <= 0:
            return
        self.is_animating = True
        def _step(count):
            nonlocal steps
            if count <= 0:
                self.is_animating = False
                return
            self.canvas.move(tag, step_dx, step_dy)
            self.root.update()
            self.root.after(25, lambda: _step(count-1))
        _step(steps)

    def step(self):
        if self.is_animating:
            return
        if self.move_index >= len(self.moves):
            return
        frm, to = self.moves[self.move_index]
        if not self.pegs[frm]:
            # nothing to move (shouldn't happen)
            self.move_index += 1
            return
        disk = self.pegs[frm].pop()
        self.pegs[to].append(disk)

        # animate disk: up -> across -> down
        tag = f"disk_{disk}"
        # current top location (peg frm)
        disk_height = 20
        # compute positions
        cur_x = self.pegs_x[frm]
        cur_y = self.ground_y - disk_height * len(self.pegs[to]) - disk_height - 5  # approximate current top

        # target x,y
        target_x = self.pegs_x[to]
        target_y = self.ground_y - disk_height * len(self.pegs[to]) - 5

        # 3-phase move
        up_y = self.ground_y - self.peg_height - 30

        def phase_down():
            # move down to target_y
            self.move_disk_to_tag(tag, target_x, target_y)
            self.root.after(self.speed_var.get(), after_move)

        def phase_across():
            # move across to target_x at up_y
            self.move_disk_to_tag(tag, target_x, up_y)
            # wait for animation to finish
            self.root.after(self.speed_var.get(), phase_down)

        def phase_up():
            # move up above peg
            self.move_disk_to_tag(tag, cur_x, up_y)
            self.root.after(self.speed_var.get(), phase_across)

        # start phases
        phase_up()

        self.move_index += 1
        self.update_status()

        # if auto_play then schedule next
        if self.auto_play:
            self.root.after(self.speed_var.get() * 2 + 50, self.step)

    def update_status(self):
        total = len(self.moves)
        self.status_label.config(text=f"Move: {self.move_index} / {total}   Minimal: {2**self.n - 1}")

    def toggle_auto(self):
        if self.is_animating:
            return
        self.auto_play = not self.auto_play
        if self.auto_play:
            self.auto_btn.config(text="Pause")
            # start auto
            if self.move_index < len(self.moves):
                self.step()
        else:
            self.auto_btn.config(text="Auto Play")


if __name__ == '__main__':
    root = tk.Tk()
    app = TowerOfHanoiApp(root)
    root.mainloop()
