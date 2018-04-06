# Techbelife_Wechat

[![Build Status](https://travis-ci.org/JEVEM624/Techbelife_Wechat.svg?branch=master)](https://travis-ci.org/JEVEM624/Techbelife_Wechat) [![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)


## Introduction

A robot for the Wechat,Through WeChat Official Accounts platform and Hubei University of Technology teaching system, Turing robot connection, in order to achieve a simple and quick check of grades, Schedules, daily chat and other functions



## How to use

1.Clone this project

```bash
git clone https://github.com/JEVEM624/Techbelife_Wechat.git
cd ./Techbelife_Wechat
pip install -r requirements.txt
chmod a+x run.sh stop.sh
```
2.Change Config.py

- **WechatToke**:WeChat Official Accounts platform token

- **TulingApiKey**: Turing Robot Apikey

- **Beginday**:Semester start date

3.Running

```bash
./run.sh

```
Default listening 5002 port

4.Stopping

```bash
./stop.sh
```