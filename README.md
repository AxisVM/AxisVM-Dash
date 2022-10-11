# **AxisVM-Dash**
Template repo for interactive dashboards using AxisVM as a batch process.

This repository does not accept pull request, **use it as a template to start new projects.** 

![Alt text](capture.png?raw=true "Title")

## **Overview**

The repo contains a minimal webapp built with Plotly Dash. It provides examples to almost all basic components necessary to build interactive webapps with high-quality visualizations of AxisVM calculations, such as

* examples for usage of basic Dash compoments to build an interactive dashboard with callbacks and advanced event handling, including
  * input components of various kinds in the form of a collapsable navigation panel
  * a detailed navigation bar 
  * facilities for 2d and 3d visualizations using `Plotly`
  * a table that reacts to user interaction (click the cells to update the plot)

* calculation of a single-supported rectangular plate with **PyAxisVM**, the official python package for **AxisVM**

* a communication solution between the frontend and the backend using Python's `threading` library

## **Usage**

It is highly recommended to create a dedicated virtual enviroment for every new project. Using the built-in `venv` package:

```console
>>> python -m venv .venv
```

then activate the enviroment with

```console
>>> .\.venv\Scripts\activate
```

To update `pip` type

```console
>>> python -m pip install --upgrade pip
```

Install the dependencies from `requirements.txt`

```console
>>> pip install -r requirements.txt
```

To launch the application locally, type

```console
>>> python app.py
```

## **Notes**

It worths noting that Dash:

* has an enterprise level solution that allows for low-code to no-code development

* integrates well with Snowflake, a cloud-based data warehouse service offered by Amazon Web Services

The repo contains some files for deployment on production scale WSGI servers. If you only want to deploy locally, ignore these. 

## **Issues**

1) At the moment the 2d contour plot is a little bit ugly. This is because nodal values are queried only at the corner nodes of 6-noded triangle elements used in **AxisVM**, and this makes the point-based approximation (it doesn't use the topology) a bit awkward.
   
2) Currently only displacement components are plotted. This is because internal forces can only be queried element-wise. There are two possible solutions for this:
   * implement smoothing
   * use per-element colouring of cells

I'll solve these issues, but the soluton requires some work to be done on the **PyAxisVM** package.

## **Resources**

* Plotly Dash
  * https://dash.plotly.com/
  * https://dash-bootstrap-components.opensource.faculty.ai/

* AxisVM python package
  * https://github.com/AxisVM/pyaxisvm

* Themes and CSS customization
  * https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/
  * https://bootswatch.com/

