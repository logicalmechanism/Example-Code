"""
p2p automated market maker
"""
import random
import itertools
import matplotlib.pyplot as plt

def evolve(Ra, Da, Rb, Db):
    Ra = Ra - Da
    Rb = Rb + Db
    return Ra, Rb

def findsubsets(s, n):
    return list(itertools.combinations(s, n))

def caluclate_amount(X, a, b, g):
    return -(b*X) / (g*(X-a))

def select_token_pair(reserves):
    """
    Select a random pair of tokens from the liquidity pool.
    """
    tokenA = random.randint(0, nTokens-1)
    tokenB = random.randint(0, nTokens-1)
    while tokenB == tokenA:
        tokenB = random.randint(0, nTokens-1)
    return tokenA, tokenB

def get_market_prices(tokens, reserves):
    """
    Find all pairs and return a dict of every market price.
    """
    pairs = findsubsets(tokens, 2)
    prices = {}
    for t in tokens:
        prices[t] = {}
    for pair in pairs:
        market_price = reserves[pair[1]]/reserves[pair[0]]
        prices[pair[0]][pair[1]] = market_price
        prices[pair[1]][pair[0]] = 1/market_price
    return prices

def simulation(nTokens, gamma, transactions):
    """
    Run a market simulation of nTokens with a gamma fee for t transactions.
    """
    reserves = [random.randint(2500000, 10000000) for _ in range(nTokens)]
    tokens = [i for i in range(nTokens)]
    # The number of transactions
    for _ in range(transactions):
        tokenA, tokenB = select_token_pair(reserves)
        print('\nTrading Token {} for Token {}'.format(tokenA, tokenB))
        reserveA = reserves[tokenA]
        reserveB = reserves[tokenB]
        # random select delta A and calculate delta B
        deltaA = random.uniform(0,reserveA//32)
        deltaB = caluclate_amount(deltaA, reserveA, reserveB, gamma)
        reserveA, reserveB = evolve(reserveA, deltaA, reserveB, deltaB)
        # Update Reserve
        reserves[tokenA] = reserveA
        reserves[tokenB] = reserveB
        market_price = get_market_prices(tokens, reserves)
        print('Market Prices After Trade')
        print(market_price)
        # print(market_price[0][1])

if __name__ == "__main__":
    gamma = 1 # feeless
    nTokens = 2
    transactions = 1000
    simulation(nTokens, gamma, transactions)
