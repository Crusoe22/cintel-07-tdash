# Import necessary libraries and modules
import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 

from shinywidgets import render_bokeh
from bokeh.plotting import figure
from palmerpenguins import load_penguins

# Load the penguins dataset
df = palmerpenguins.load_penguins()

# Set page options for the UI
ui.page_opts(title="Palmer Penguins Dashboard", fillable=True)

# Create sidebar with filter controls
with ui.sidebar(title="Filter Data Controls"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    # Bokeh input
    ui.input_selectize(
    "var", "Select variable",
    choices=["bill_length_mm", "body_mass_g"]
    )
    # Add horizontal rule and links to external resources
    ui.hr()
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )


# Create layout for displaying penguin statistics
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


# Create layout for displaying statistics
with ui.layout_columns():

    with ui.card(full_screen=True):
        ui.card_header("Bokeh Chart")
        @render_bokeh
        def hist():

            p = figure(x_axis_label=input.var(), y_axis_label="count")
            bins = load_penguins()[input.var()].value_counts().sort_index()
            p.quad(
                top=bins.values,
                bottom=0,
                left=bins.index - 0.5,
                right=bins.index + 0.5,
            )
            return p

    # Card for displaying summary statistics of penguin data
    with ui.card(full_screen=True):
        ui.card_header("Penguin Statistic Data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


#ui.include_css(app_dir / "styles.css")


# Define reactive function to filter the dataset based on user inputs
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
