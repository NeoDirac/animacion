from manim import *
import numpy as np

config.assets_dir = "assets"

class Robot(SVGMobject):
    def __init__(self, **kwargs):
        super().__init__("robot.svg", **kwargs)
        self.set(width=1.2)
        self.set_fill(WHITE)
        self.set_stroke(BLACK, width=2)

# 1. INTRO
class IntroScene(Scene):
    def construct(self):
        self.wait(0.5)
        title = Text("¿FOR o WHILE? ¡La Gran Duda!", font_size=54, color=BLUE)
        self.play(Write(title), run_time=2.5)
        self.wait(2)
        meme = ImageMobject("meme_intro.png").scale(1.3).next_to(title, DOWN)
        self.play(FadeIn(meme), run_time=1.5)
        self.wait(7)
        self.play(FadeOut(title), FadeOut(meme))
        self.wait(1)

# 2. FOR
class ForScene(Scene):
    def construct(self):
        self.wait(1)
        title = Text("FOR: Pasos Exactos", font_size=44).to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(1.7)

        robot = Robot().move_to(LEFT * 4 + DOWN * 1)
        target = Circle(radius=0.5, color=RED, fill_opacity=0.6).move_to(RIGHT * 4 + DOWN * 1)
        self.add(robot, target)

        pasos = []
        for i in range(5):
            pos = interpolate(LEFT * 4 + DOWN * 1, RIGHT * 4 + DOWN * 1, i / 4)
            huella = Dot(pos, radius=0.13, color=GRAY)
            pasos.append(huella)
            self.add(huella)

        self.wait(2)

        # Corregido: el contador SIEMPRE muestra el número correcto y solo uno por paso
        
        for i, huella in enumerate(pasos):
         # 1. Mueve el robot y resalta la huella primero
            self.play(
                robot.animate.move_to(huella.get_center()),
                FadeToColor(huella, YELLOW),
                run_time=1.3
            )   
             # 2. Luego muestra el número en la nueva posición
            step_text = Text(f"{i+1}", font_size=32).next_to(robot, UP)
            self.play(Write(step_text))
            self.wait(1.1)
            self.remove(step_text)

        self.wait(2)
        code = Code(
            "for_loop.py",
            tab_width=4,
            background="window",
            language="python"
        ).to_corner(DOWN+LEFT)
        self.play(FadeIn(code), run_time=1.2)
        self.wait(8)  # Tiempo largo para leer el código

        meme = ImageMobject("meme_for.png").scale(1.12).to_corner(DOWN+RIGHT)
        self.play(FadeIn(meme), run_time=1.5)
        self.wait(7)
        self.play(FadeOut(code), FadeOut(meme), FadeOut(robot), FadeOut(target), *[FadeOut(h) for h in pasos], FadeOut(title))
        self.wait(1.5)

# 3. WHILE
class WhileScene(Scene):
    def construct(self):
        self.wait(1)
        title = Text("WHILE: Hasta Alcanzar", font_size=44).to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(1.7)

        robot = Robot().move_to(LEFT * 4 + DOWN * 1)
        offset = np.random.uniform(3.2, 5.7)
        target = Circle(radius=0.5, color=RED, fill_opacity=0.6).move_to(RIGHT * offset + DOWN * 1)
        self.add(robot, target)
        pasos = []
        steps = 0

        self.wait(2)
        while np.linalg.norm(robot.get_center() - target.get_center()) > 1.2:
            pos = robot.get_center() + RIGHT * 0.8
            huella = Dot(pos, radius=0.13, color=GRAY)
            pasos.append(huella)
            step_text = Text(f"{steps+1}", font_size=32).next_to(robot, UP)
            self.play(
                robot.animate.move_to(pos),
                FadeIn(huella),
                Write(step_text),
                run_time=1
            )
            self.wait(0.9)
            self.remove(step_text)
            steps += 1

        self.wait(2)
        code = Code(
            "while_loop.py",
            tab_width=4,
            background="window",
            language="python"
        ).to_corner(DOWN+LEFT)
        self.play(FadeIn(code), run_time=1.2)
        self.wait(8)
        meme = ImageMobject("meme_while.png").scale(1.12).to_corner(DOWN+RIGHT)
        self.play(FadeIn(meme), run_time=1.5)
        self.wait(7)
        self.play(FadeOut(code), FadeOut(meme), FadeOut(robot), FadeOut(target), *[FadeOut(h) for h in pasos], FadeOut(title))
        self.wait(1.5)

# 4. COMPARACION
class ComparacionScene(Scene):
    def construct(self):
        self.wait(1)
        title = Text("FOR vs WHILE", font_size=48, color=GREEN).to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(1.5)

        left_rect = Rectangle(width=6, height=4).shift(LEFT * 3 + DOWN * 0.5)
        right_rect = Rectangle(width=6, height=4).shift(RIGHT * 3 + DOWN * 0.5)
        self.add(left_rect, right_rect)

        robot_for = Robot().move_to(left_rect.get_left() + RIGHT * 1 + DOWN * 1)
        target_for = Circle(radius=0.4, color=RED, fill_opacity=0.6).move_to(left_rect.get_right() + LEFT * 1 + DOWN * 1)
        self.add(robot_for, target_for)
        self.wait(1.2)
        for i in range(3):
            self.play(robot_for.animate.move_to(robot_for.get_center() + RIGHT * 1.5), run_time=1.1)
            self.wait(0.8)

        robot_while = Robot().move_to(right_rect.get_left() + RIGHT * 1 + DOWN * 1)
        offset = np.random.uniform(2.2, 2.7)
        target_while = Circle(radius=0.4, color=RED, fill_opacity=0.6).move_to(right_rect.get_left() + RIGHT * (1+offset) + DOWN * 1)
        self.add(target_while)
        self.wait(1.2)
        while np.linalg.norm(robot_while.get_center() - target_while.get_center()) > 1.0:
            self.play(robot_while.animate.move_to(robot_while.get_center() + RIGHT * 0.5), run_time=0.8)
            self.wait(0.5)

        self.wait(3)
        meme = ImageMobject("meme_comparacion.png").scale(1.15).to_corner(DOWN)
        self.play(FadeIn(meme), run_time=1.5)
        self.wait(8)
        self.play(*[FadeOut(m) for m in [title, left_rect, right_rect, robot_for, target_for, robot_while, target_while, meme]])
        self.wait(1.7)

# 5. CONCLUSION
class ConclusionScene(Scene):
    def construct(self):
        self.wait(1)
        title = Text("¡Recuerda la Diferencia!", font_size=44, color=PURPLE)
        robot = Robot().scale(1.6)
        self.play(Write(title), FadeIn(robot), run_time=2)
        self.play(robot.animate.shift(DOWN * 0.5), run_time=1)
        self.play(Rotate(robot, angle=2*PI), run_time=2.6)
        texto_final = Text("FOR: Conteo exacto\nWHILE: Condición", font_size=36).next_to(robot, DOWN)
        self.play(Write(texto_final), run_time=1.5)
        self.wait(3)
        call_to_action = Text("¡Dale like y suscríbete xd", font_size=30, color=YELLOW).next_to(texto_final, DOWN)
        self.play(Write(call_to_action), run_time=1.5)
        self.wait(7)
        self.play(FadeOut(title), FadeOut(robot), FadeOut(texto_final), FadeOut(call_to_action))
        self.wait(1.5)



class ForDemo(Scene):
    def construct(self):
        # Título
        title = Text("FOR: Avanza 5 pasos", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(title), run_time=1)
        self.wait(0.5)

        # Código fuente
        code = Code(
            "for_loop.py",
            tab_width=4,
            background="window",
            language="python"
        ).scale(0.85).to_edge(LEFT)
        self.play(FadeIn(code), run_time=1)
        self.wait(0.5)

        # Variables visuales
        var_text = Text("paso = 0", font_size=34, color=YELLOW).to_corner(UP+RIGHT)
        self.play(FadeIn(var_text))
        self.wait(0.4)

        # Área de "consola" para prints
        print_area = VGroup()
        print_base = code.get_right() + RIGHT * 1.2 + UP * 1.3

        # Ciclo for didáctico
        for i in range(5):
            # Actualiza variable
            new_var = Text(f"paso = {i}", font_size=34, color=YELLOW).to_corner(UP+RIGHT)
            self.play(ReplacementTransform(var_text, new_var), run_time=0.18)
            var_text = new_var
            self.wait(0.15)

            # Simula print en consola
            print_line = Text(f"Paso {i+1}", font_size=30, color=GREEN)
            print_line.move_to(print_base + DOWN * 0.43 * i)
            self.play(Write(print_line), run_time=0.20)
            print_area.add(print_line)
            self.wait(0.13)

        # Print final
        print_final = Text("¡Objetivo alcanzado!", font_size=30, color=ORANGE)
        print_final.move_to(print_base + DOWN * 0.43 * 5 + DOWN * 0.20)
        self.play(Write(print_final), run_time=0.25)
        print_area.add(print_final)
        self.wait(1.7)

        # Fade out todo
        self.play(
            FadeOut(title), FadeOut(code), FadeOut(var_text),
            *[FadeOut(linea) for linea in print_area]
        )
        self.wait(0.3)

class WhileDemo(Scene):
    def construct(self):
        # Título
        title = Text("WHILE: Hasta llegar al objetivo", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(title), run_time=1)
        self.wait(0.5)

        # Código fuente
        code = Code(
            "while_loop.py",
            tab_width=4,
            background="window",
            language="python"
        ).scale(0.85).to_edge(LEFT)
        self.play(FadeIn(code), run_time=1)
        self.wait(0.5)

        # Variables iniciales
        objetivo = 12
        paso = 0

        paso_text = Text(f"paso = {paso}", font_size=34, color=YELLOW).to_corner(UP+RIGHT)
        objetivo_text = Text(f"objetivo = {objetivo}", font_size=34, color=WHITE).next_to(paso_text, DOWN, aligned_edge=RIGHT)
        self.play(FadeIn(paso_text), FadeIn(objetivo_text))
        self.wait(0.3)

        cond_color = GREEN if paso < objetivo else RED
        cond_text = Text(f"paso < objetivo → {paso < objetivo}", font_size=28, color=cond_color)
        cond_text.next_to(objetivo_text, DOWN, aligned_edge=RIGHT)
        self.play(FadeIn(cond_text))
        self.wait(0.3)

        print_area = VGroup()
        print_base = code.get_right() + RIGHT * 1.2 + UP * 1.3

        idx_print = 0
        while paso < objetivo:
            paso += 1
            new_paso_text = Text(f"paso = {paso}", font_size=34, color=YELLOW).to_corner(UP+RIGHT)
            self.play(ReplacementTransform(paso_text, new_paso_text), run_time=0.13)
            paso_text = new_paso_text

            # Actualiza condición booleana
            cond_color = GREEN if paso < objetivo else RED
            new_cond_text = Text(f"paso < objetivo → {paso < objetivo}", font_size=28, color=cond_color)
            new_cond_text.next_to(objetivo_text, DOWN, aligned_edge=RIGHT)
            self.play(ReplacementTransform(cond_text, new_cond_text), run_time=0.12)
            cond_text = new_cond_text

            # Simula print en consola
            print_line = Text(f"Paso {paso}", font_size=30, color=GREEN)
            print_line.move_to(print_base + DOWN * 0.39 * idx_print)
            self.play(Write(print_line), run_time=0.15)
            print_area.add(print_line)
            self.wait(0.09)
            idx_print += 1

        # Print final
        print_final = Text("¡Objetivo detectado!", font_size=30, color=ORANGE)
        print_final.move_to(print_base + DOWN * 0.39 * idx_print + DOWN * 0.18)
        self.play(Write(print_final), run_time=0.22)
        print_area.add(print_final)
        self.wait(1.8)

        self.play(
            FadeOut(title), FadeOut(code),
            FadeOut(paso_text), FadeOut(objetivo_text), FadeOut(cond_text),
            *[FadeOut(linea) for linea in print_area]
        )
        self.wait(0.3)