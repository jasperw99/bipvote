import argparse
import requests
import numpy as np

def sendVoteAndOpinion(vote):
    files = {'opinion': open('example.wav', 'rb')}
    data = {'key': 'bipvote', 'vote_or_opinion': '2', 'choice': vote}
    r = requests.post('https://bipvote.ml/vote/', files=files, data=data)
    print(r)

def sendVote(vote):
    data = {'key': 'bipvote', 'vote_or_opinion': '0', 'choice': vote}
    r = requests.post('https://bipvote.ml/vote/', data=data)

def sendOpinion():
    files = {'opinion': open('example.wav', 'rb')}
    data = {'key': 'bipvote', 'vote_or_opinion': '1', 'choice':'1'}
    r = requests.post('https://bipvote.ml/vote/', files=files, data=data)
    print(r)

def sendMultiple(r, t, vote):
    choices = ['1', '0']
    for i in range(r):
        if t == 0:
            sendVote(vote)
        elif t == 1:
            sendOpinion()
        elif t == 2:
            sendVoteAndOpinion(vote)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', nargs=1, type=int, help="Number of repetitions", required=True)
    parser.add_argument('-t', nargs=1, type=int, help="Type of action:\n\t0: Vote\n\t1: Opinion\n\t2: Vote and opinion", required=True)
    parser.add_argument('-c', nargs=1, type=int, help="Choice, 0 for no, 1 for yes (optional)", required=False)
    args = parser.parse_args()
    r = args.r[0]
    t = args.t[0]
    if args.t[0] > 2 or args.t[0] < 0:
        print("t out of range")
        exit(1)
    elif args.r[0] < 1:
        print("r should be bigger than 0")
        exit(1)
    
    if args.c is not None:
        c = args.c[0]
    else:
        c = '1'

    sendMultiple(r, t, c)

    

