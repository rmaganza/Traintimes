# Traintimes 🚆

Final project for the Data Management and Visualization course by:

*Giulia Chiaretti*

*Federica Fiorentini*

*Riccardo Maganza*

*Alberto Monaco*

**Data Science MSc, Università degli Studi di Milano-Bicocca**.

## Goals 🎯

Our aim was to collect and analyze data about delays in high speed lines (Frecce) in Italy, store them in a meaningful way, and create some dashboards after that.
We also tried our way with data integration by adding weather information to our data to hopefully find some kind of relationship.

## Tools 🛠

Throughout this whole project, we learned what it's like to use outdated infrastructures (Python 2.x locked VMs), work with terrible APIs (Viaggiatreno) and unreliable data sources (HERE Weather).
After some trial and error, this was the stack:

* Processing: Python 2.7
* Streaming: Kafka
* Data Storage: MongoDB
* Dashboards: Microsoft PowerBI

This repository contains the backend.

The software is very fault-tolerant and stable. 

* The *api* module does the parsing and interfaces with [the monstrosity that is Viaggiatreno](https://medium.com/@albigiu/trenitalia-shock-non-crederete-mai-a-queste-api-painful-14433096502c);
* The *streamprocessing* module actually sends the data to Kafka and from there to Mongo;
* The *batch_jobs* module contains some tedious jobs which we had to run before we actually had our streaming platform up (such as getting a list of all train stations in Italy);
* The *exceptionhandling* module deals with the unexpected, trying to be accomodating with problems in the API while also sending a mail to the sysadmin if something eventually breaks.

## Dashboards

The final report, together with the data visualizations we produces is available [here](https://rmaganza.github.io/dataviz-streamtrains/).
