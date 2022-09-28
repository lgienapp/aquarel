import sys
sys.path.append('../aquarel')

import unittest
import matplotlib.pyplot as plt
from aquarel import Theme
from cycler import cycler

class TestTheme(unittest.TestCase):
    def setUp(self):
        self.theme = Theme(name="test", description="A test theme.")
        print("\n***** set up *****")
        print("> set up a test theme")


    def test_set_overrides(self):
        print(f"\n***** set overrides *****")
        options = [{"lines.dash_joinstyle": "bevel"}, {"boxplot.flierprops.color": "red", "ytick.minor.visible": False}]
        for option in options:
            for key, value in option.items():
                print(f'> set "{key}" to be {value}')
                with self.theme.set_overrides(option):
                    print(f'>> check if plt.rcParams["{key}"] == {value}')
                    self.assertEqual(value, plt.rcParams[key])   


    def test_set_title(self):
        def title_test(parameter, options):
            print(f"\n***** title.{parameter} *****")
            for option in options:
                print(f"> set title.{parameter} to be {option}")
                with self.theme.set_title(**{parameter: option}):
                    for param in self.theme._rcparams_mapping["title"][parameter]:
                        print(f'>> check if plt.rcParams["{param}"] == {option}')
                        self.assertEqual(option, plt.rcParams[param])   

        title_test("location", self.theme._horizontal_alignment_options)
        title_test("pad", [0, 0.5, 1.5, 5])
        title_test("size", self.theme._font_size_options)
        title_test("weight", self.theme._font_weight_options)


    def test_set_grid(self):
        def grid_test(parameter, options):
            print(f"\n***** grid.{parameter} *****")
            for option in options:
                print(f"> set grid.{parameter} to be {option}")
                with self.theme.set_grid(**{parameter: option}):
                    for param in self.theme._rcparams_mapping["grid"][parameter]:
                        print(f'>> check if plt.rcParams["{param}"] == {option}')
                        self.assertEqual(option, plt.rcParams[param])   

        grid_test("draw", [True, False])
        grid_test("axis", self.theme._axis_options)
        grid_test("ticks", self.theme._tick_options)
        grid_test("alpha", [0, 0.5, 1])
        grid_test("style", self.theme._line_style_options)
        grid_test("width", [0, 0.5, 1.5, 5])


    def test_set_axes(self):
        def axes_test(parameter, options):
            print(f"\n***** axes.{parameter} *****")
            for option in options:
                print(f"> set axes.{parameter} to be {option}")
                with self.theme.set_axes(**{parameter: option}):
                    for param in self.theme._rcparams_mapping["axes"][parameter]:
                        print(f'>> check if plt.rcParams["{param}"] == {option}')
                        self.assertEqual(option, plt.rcParams[param])   

        axes_test("width", [0, 0.5, 1.5, 5])
        axes_test("top", [True, False])
        axes_test("bottom", [True, False])
        axes_test("left", [True, False])
        axes_test("right", [True, False])
        axes_test("xmargin", [0.01, 0.05, 0.15, 0.5])
        axes_test("ymargin", [0.01, 0.05, 0.15, 0.5])
        axes_test("zmargin", [0.01, 0.05, 0.15, 0.5])


    def test_set_color(self):
        def color_test(parameter, options):
            print(f"\n***** colors.{parameter} *****")
            for option in options:
                print(f"> set colors.{parameter} to be {option}")
                with self.theme.set_color(**{parameter: option}):
                    for param in self.theme._rcparams_mapping["colors"][parameter]:
                        print(f'>> check if plt.rcParams["{param}"] == {option}')
                        self.assertEqual(option, plt.rcParams[param])   

        color_test("figure_background_color", ["red", "#ff0000"])
        color_test("plot_background_color", ["red", "#ff0000"])
        color_test("text_color", ["red", "#ff0000"])
        color_test("axes_color", ["red", "#ff0000"])
        color_test("axes_label_color", ["red", "#ff0000"])
        color_test("line_color", ["red", "#ff0000"])
        color_test("grid_color", ["red", "#ff0000"])
        color_test("tick_color", ["red", "#ff0000"])
        color_test("tick_label_color", ["red", "#ff0000"])
        color_test("legend_border_color", ["red", "#ff0000"])
        color_test("legend_background_color", ["red", "#ff0000"])

        # color_test("palette", [cycler("color", ["red", "green"])]) doesn't work for some reason
        print(f"\n***** colors.palette *****")
        for option in [cycler("color", ["red", "green"]), cycler("color", ["#ff0000", "#00ff00"])]:
            print(f"> set colors.palette to be {option}")
            with self.theme.set_color(**{"palette": option}):
                param = self.theme._rcparams_mapping["colors"]["palette"]
                print(f'>> check if plt.rcParams["{param}"] == {option}')
                self.assertEqual(option, plt.rcParams[param])   


    def test_set_axis_labels(self):
        def axis_labels_test(parameter, options):
            print(f"\n***** axis_labels.{parameter} *****")
            for option in options:
                print(f"> set axis_labels.{parameter} to be {option}")
                with self.theme.set_axis_labels(**{parameter: option}):
                    for param in self.theme._rcparams_mapping["axis_labels"][parameter]:
                        print(f'>> check if plt.rcParams["{param}"] == {option}')
                        self.assertEqual(option, plt.rcParams[param])   

        axis_labels_test("pad", [0, 5, 10])
        axis_labels_test("size", self.theme._font_size_options)
        axis_labels_test("weight", self.theme._font_weight_options)
 

    def test_set_tick_labels(self):
        def tick_labels_test(parameter, options):
            print(f"\n***** tick_labels.{parameter} *****")
            for option in options:
                print(f"> set tick_labels.{parameter} to be {option}")
                with self.theme.set_tick_labels(**{parameter: option}):
                    for param in self.theme._rcparams_mapping["tick_labels"][parameter]:
                        print(f'>> check if plt.rcParams["{param}"] == {option}')
                        self.assertEqual(option, plt.rcParams[param])   

        # This test does not work and it is mentioned in issue #25
        # tick_labels_test("location", self.theme._location_options)
        tick_labels_test("size", self.theme._font_size_options)
        tick_labels_test("top", [True, False])
        tick_labels_test("bottom", [True, False])
        tick_labels_test("left", [True, False])
        tick_labels_test("right", [True, False])

    
    def test_set_ticks(self):
        def ticks_test(parameter, options):
            print(f"\n***** ticks.{parameter} *****")
            for option in options:
                print(f"> set ticks.{parameter} to be {option}")
                with self.theme.set_ticks(**{parameter: option}):
                    for param in self.theme._rcparams_mapping["ticks"][parameter]:
                        print(f'>> check if plt.rcParams["{param}"] == {option}')
                        self.assertEqual(option, plt.rcParams[param])   

        ticks_test("x_align", self.theme._horizontal_alignment_options)
        ticks_test("y_align", self.theme._vertical_alignment_options)
        ticks_test("direction", self.theme._direction_options)
        ticks_test("draw_minor", [True, False])
        ticks_test("width_major", [0, 0.5, 1.5, 5])
        ticks_test("width_minor", [0, 0.5, 1.5, 5])
        ticks_test("size_major", [0, 0.5, 1.5, 5])
        ticks_test("size_major", [0, 0.5, 1.5, 5])
        ticks_test("pad_minor", [0, 0.5, 1.5, 5])
        ticks_test("pad_minor", [0, 0.5, 1.5, 5])
  

    def test_set_lines(self):
        def lines_test(parameter, options):
            print(f"\n***** lines.{parameter} *****")
            for option in options:
                print(f"> set lines.{parameter} to be {option}")
                with self.theme.set_lines(**{parameter: option}):
                    for param in self.theme._rcparams_mapping["lines"][parameter]:
                        print(f'>> check if plt.rcParams["{param}"] == {option}')
                        self.assertEqual(option, plt.rcParams[param])   

        lines_test("style", self.theme._line_style_options)
        lines_test("width", [0, 0.5, 1.5, 5])


    def test_set_font(self):
        def font_test(parameter, options):
            print(f"\n***** fonts.{parameter} *****")
            for option in options:
                print(f"> set fonts.{parameter} to be {option}")
                with self.theme.set_font(**{"sans_serif" if parameter == "sans-serif" else parameter : option}):
                    for param in self.theme._rcparams_mapping["fonts"][parameter]:
                        print(f'>> check if plt.rcParams["{param}"] == {option}')
                        if parameter == "family":
                            self.assertEqual([option], plt.rcParams[param])   
                        else:
                            self.assertEqual(option, plt.rcParams[param])   

        font_test("family", self.theme._font_family_options)
        font_test("cursive", [["Apple Chancery", "Textile"]])
        font_test("fantasy", [["Chicago", "Charcoal"]])
        font_test("monospace", [["DejaVu Sans Mono", "Bitstream Vera Sans Mono"]])
        font_test("sans-serif", [["DejaVu Sans", "Bitstream Vera Sans"]])
        font_test("serif", [["DejaVu Serif", "Bitstream Vera Serif"]])
        font_test("size", [0, 5, 15, 50])
        font_test("stretch", self.theme._font_stretch_options)
        font_test("style", self.theme._font_style_options)
        font_test("variant", self.theme._font_variant_options)
        font_test("weight", self.theme._font_weight_options)


    def test_set_legend(self):
        def legend_test(parameter, options):
            print(f"\n***** legend.{parameter} *****")
            for option in options:
                print(f"> set legend.{parameter} to be {option}")
                with self.theme.set_legend(**{parameter: option}):
                    for param in self.theme._rcparams_mapping["legend"][parameter]:
                        print(f'>> check if plt.rcParams["{param}"] == {option}')
                        self.assertEqual(option, plt.rcParams[param])   

        legend_test("location", self.theme._legend_location_options)
        legend_test("round", [True, False])
        legend_test("shadow", [True, False])
        legend_test("title_size", self.theme._font_size_options)
        legend_test("text_size", self.theme._font_size_options)
        legend_test("alpha", [0, 0.5, 1])
        legend_test("marker_scale", [0, 0.5, 1.5, 5])
        legend_test("padding", [0, 0.5, 1.5, 5])
        legend_test("margin", [0, 0.5, 1.5, 5])
        legend_test("spacing", [0, 0.5, 1.5, 5])


if __name__ == "__main__":
    unittest.main()