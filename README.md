# LAB TREE
a simple tool to download, curate and visualize a researcher's publications history

Lab tree is built using **Dash**.
First create an environment with `dash`, `dash_bootstrap_components`
and `pandas`

then run `python app_navbar.py` to start the program.

# TO DO

For now, there are two active tabs: load articles and review articles

Load articles uses the scholarly package to fetch from the google scholar API. It should eventually allow the user to download the data in tabular format, ideally using the [download button](https://dash.plotly.com/dash-core-components/download) from Dash

Then, in Review articles, we ask the user to curate the articles (make sure that the abstracts/ authors lists are correct).
For now, the page comes pre-loaded with the publications of Naama Barkai. Instead, the user should 
be able to load from any tsv using the [upload component](https://dash.plotly.com/dash-core-components/upload) from Dash

Finally, we will integrate the students visualisations in the "visualise articles" tab.

            