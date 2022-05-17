""""""  		  	   		  	  			  		 			     			  	 
"""Assess a betting strategy.  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  	  			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		  	  			  		 			     			  	 
All Rights Reserved  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
Template code for CS 4646/7646  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  	  			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		  	  			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		  	  			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		  	  			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		  	  			  		 			     			  	 
or edited.  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		  	  			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		  	  			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  	  			  		 			     			  	 
GT honor code violation.  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
-----do not edit anything above this line---  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
Student Name: Tiandi Wu (replace with your name)  		  	   		  	  			  		 			     			  	 
GT User ID: twu411  (replace with your User ID)  		  	   		  	  			  		 			     			  	 
GT ID: 596568372 (replace with your GT ID)  		  	   		  	  			  		 			     			  	 
"""  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
def author():  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    :return: The GT username of the student  		  	   		  	  			  		 			     			  	 
    :rtype: str  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    return "twu411"  # replace tb34 with your Georgia Tech username.
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
def gtid():  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    :return: The GT ID of the student  		  	   		  	  			  		 			     			  	 
    :rtype: int  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    return 596568372  # replace with your GT ID number
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
def get_spin_result(win_prob):  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    :param win_prob: The probability of winning  		  	   		  	  			  		 			     			  	 
    :type win_prob: float  		  	   		  	  			  		 			     			  	 
    :return: The result of the spin.  		  	   		  	  			  		 			     			  	 
    :rtype: bool  		  	   		  	  			  		 			     			  	 
    """
    result = False  		  	   		  	  			  		 			     			  	 
    if np.random.random() <= win_prob:  		  	   		  	  			  		 			     			  	 
        result = True  		  	   		  	  			  		 			     			  	 
    return result  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
def test_code():  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    Method to test your code  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    win_prob = 18.0/38.0  # set appropriately to the probability of a win
    np.random.seed(gtid())  # do this only once  		  	   		  	  			  		 			     			  	 
    #print(get_spin_result(win_prob))  # test the roulette spin
    # add your code here to implement the experiments
    _10times = n_episode(10)
    _1000times = n_episode(1000)
    _1000timeslimited = n_episodewithlim(1000)
    _10df = get_dataframe(_10times)
    _1000df = get_dataframe(_1000times)
    _1000dflim = get_dataframe(_1000timeslimited)
    cal_plot1(_10df)
    cal_plot2(_1000df)
    cal_plot3(_1000dflim)
    """
    for i in _1000timeslimited[:, -1]:
        if i != 80 and i != -256:
            print (i)
    print(countertoreachx(_1000times, 80))
    print(countertoreachx(_1000timeslimited, 80))
    print(countertoreachx(_1000timeslimited, -256))
    """
def gambling_simulator():
    """ a gambling simulator of each episode"""
    episode_winnings = 0
    counter = 0
    record_winnings = [0, ]

    while episode_winnings < 80 and counter < 1001:
        won = False
        bet_amount = 1
        while (not won) and counter < 1001:
            won = get_spin_result(18.0/38.0)
            if won == True:
                episode_winnings = episode_winnings + bet_amount
                if episode_winnings >= 80:
                    episode_winnings = 80
            else:
                episode_winnings = episode_winnings - bet_amount
                bet_amount = bet_amount * 2
            record_winnings.append(episode_winnings)
            counter = counter + 1
            """fill all the blank after reaching 80 dollars"""
    while len(record_winnings) < 1001:
        record_winnings.append(80)
    return record_winnings
def gambling_simulatorlim():
    """ a gambling simulator with a limitation, return a 1000*1 ndarray to record the money"""
    episode_winnings = 0
    record_winnings = [0, ]
    while ((episode_winnings < 80 and len(record_winnings) < 1001) and episode_winnings > -256):

        won = False
        bet_amount = 1
        while (not won) and len(record_winnings) < 1001 and bet_amount > 0:
            won = get_spin_result(18.0 / 38.0)
            if won == True:
                episode_winnings = episode_winnings + bet_amount
                if episode_winnings >= 80:
                    episode_winnings = 80

            else:
                episode_winnings = episode_winnings - bet_amount
                bet_amount = min((bet_amount * 2), (256 + episode_winnings))
            record_winnings.append(episode_winnings)


    while len(record_winnings) < 1001:
        record_winnings.append(record_winnings[-1])
    return record_winnings


def n_episode(num):
    """record the data of num times trial"""
    a = np.empty((num, 1001), dtype=int)
    for i in range (num):
        a[i] = gambling_simulator()
    return a
def n_episodewithlim(number):
    b = np.empty((number, 1001), dtype=int)
    for i in range (number):
        b[i] = gambling_simulatorlim()
    return b

def get_dataframe(thetables):
    thiscolumn = []
    for i in range (1001):
        thiscolumn.append('Spin[{}]'.format(i))
    df1 = pd.DataFrame(thetables, columns=thiscolumn)
    return df1

def cal_plot1(df):
    """ploting data for experiment 1, Figure 1, ten times trial"""
    newdf = df.T


    ax = newdf.plot(title='10 times unlimited bets' , xlim = (0,300), ylim = (-256,100), legend = True)

    ax.set_xlabel("times")
    ax.set_ylabel("winnings")
    plt.legend(labels=range(1,11))
    plt.savefig(".//images//figure1.png")
    plt.cla()

def cal_plot2(df):
    """ploting data for experiment 1, Figure 2 and 3, a thousand times trial"""

    thismean = df.mean(axis=0)
    abovemean = thismean + df.std(axis=0)
    belowmean = thismean - df.std(axis=0)
    ax = thismean.plot(title = 'mean of 1000 times unlimited bets', xlim = (0,300), ylim=(-256,100))
    ax.set_xlabel("times")
    ax.set_ylabel("winnings")
    abovemean.plot(xlim = (0,300), ylim=(-256,100))
    belowmean.plot(xlim = (0,300), ylim=(-256,100))
    plt.legend(labels= ['mean', 'upperband','lowerband'])
    plt.savefig(".//images//figure2.png")
    plt.cla()



    thismedian = df.median(axis=0)
    abovemedian = thismedian + df.std(axis=0)
    belowmedian = thismedian - df.std(axis=0)
    bx = thismedian.plot(title = 'median of 1000 times unlimited bets', xlim = (0,300), ylim=(-256,100))
    bx.set_xlabel("times")
    bx.set_ylabel("winnings")
    abovemedian.plot(xlim = (0,300), ylim=(-256,100))
    belowmedian.plot(xlim = (0,300), ylim=(-256,100))
    plt.legend(labels= ['median', 'upperband','lowerband'])
    plt.savefig(".//images//figure3.png")
    plt.cla()

def cal_plot3(df):
    """ploting data for experiment 1, Figure 4 and 5, a thousand times trial"""

    thismean = df.mean(axis=0)
    abovemean = thismean + df.std(axis=0)
    belowmean = thismean - df.std(axis=0)
    ax = thismean.plot(title = 'mean of 1000 times 256-limited bets', xlim = (0,300), ylim=(-256,100))
    ax.set_xlabel("times")
    ax.set_ylabel("winnings")
    abovemean.plot(xlim = (0,300), ylim=(-256,100))
    belowmean.plot(xlim = (0,300), ylim=(-256,100))
    plt.legend(labels= ['mean', 'upperband','lowerband'])
    plt.savefig(".//images//figure4.png")
    plt.cla()


    thismedian = df.median(axis=0)
    abovemedian = thismedian + df.std(axis=0)
    belowmedian = thismedian - df.std(axis=0)
    bx = thismedian.plot(title = 'median of 1000 times 256-limited bets', xlim = (0,300), ylim=(-256,100))
    bx.set_xlabel("times")
    bx.set_ylabel("winnings")
    abovemedian.plot(xlim = (0,300), ylim=(-256,100))
    belowmedian.plot(xlim = (0,300), ylim=(-256,100))
    plt.legend(labels= ['median', 'upperband','lowerband'])
    plt.savefig(".//images//figure5.png")
    plt.cla()


def countertoreachx (nd, x):
    "count the number of episodes that ends up with x"
    counter =0
    for i in range(0, nd.shape[0]):
        if nd[i][-1] == x:
            counter = counter + 1
    return counter


if __name__ == "__main__":  		  	   		  	  			  		 			     			  	 
    test_code()  		  	   		  	  			  		 			     			  	 
