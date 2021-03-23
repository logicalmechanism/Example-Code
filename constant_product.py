"""
p2p automated market maker

N tokens are deposited into a liquidity pool. Two random tokens are
selected. A random amount of the first token is selected to swap with
the other token. The market automatically creats a swap amount and
evolves the reserves to determines the new martket price.

A simple model of a constant product market.


Guillermo  Angeris  et  al.
An  analysis  of  Uniswap  markets. 2019. 
arXiv: https://arxiv.org/abs/1911.03380

"""
from random import randint, uniform
from itertools import combinations


def evolve(Ra, Da, Rb, Db):
    """
    Evolve the two reserves involved in the swap.
    """
    Ra = Ra - Da
    Rb = Rb + Db
    return Ra, Rb


def caluclate_amount(X, a, b, g):
    """
    See the simple calculation section.
    https://ancientkraken.gitbook.io/simple-amm/
    """
    return -(b*X) / (g*(X-a))


def select_token_pair(reserves):
    """
    Select a random pair of tokens from the liquidity pool.
    """
    tokenA = randint(0, nTokens-1)
    tokenB = randint(0, nTokens-1)
    while tokenB == tokenA:
        tokenB = randint(0, nTokens-1)
    return tokenA, tokenB


def get_market_prices(tokens, reserves):
    """
    Find all pairs and return a dict of every market price.
    """
    pairs = list(combinations(tokens, 2))
    prices = {}
    for t in tokens:
        prices[t] = {}
    for pair in pairs:
        market_price = reserves[pair[1]]/reserves[pair[0]]
        # Get price for both directions.
        prices[pair[0]][pair[1]] = market_price
        prices[pair[1]][pair[0]] = 1/market_price
    return prices


def simulation(nTokens, gamma, transactions):
    """
    Run a market simulation of nTokens with a gamma fee for t transactions.
    """
    minimum = 2.5*pow(10,7)
    maximum = 10*pow(10,7)
    reserves = [randint(minimum, maximum) for _ in range(nTokens)]
    tokens = [i for i in range(nTokens)]
    print('\nToken Labels {}'.format(tokens))
    print('Liquidity Pools {}'.format(reserves))
    print('Transaction Fee {}'.format(1-gamma))

    # The number of transactions
    for t in range(transactions):

        # Randon select two tokens
        tokenA, tokenB = select_token_pair(reserves)
        reserveA = reserves[tokenA]
        reserveB = reserves[tokenB]

        # random select delta A and calculate delta B
        deltaA = uniform(0, 1000)
        print('\nTrading {} of Token {} for Token {}'.format(deltaA, tokenA, tokenB))
        deltaB = caluclate_amount(deltaA, reserveA, reserveB, gamma)
        print('Paying {} of Token {}'.format(deltaB, tokenB))

        # Update Reserve
        reserveA, reserveB = evolve(reserveA, deltaA, reserveB, deltaB)
        reserves[tokenA] = reserveA
        reserves[tokenB] = reserveB
        market_price = get_market_prices(tokens, reserves)
        print('Market Prices After Trade')
        print(market_price)

if __name__ == "__main__":
    gamma = 1 # feeless
    nTokens = 3
    transactions = 3
    simulation(nTokens, gamma, transactions)
