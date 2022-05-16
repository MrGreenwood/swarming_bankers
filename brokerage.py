import random
import numpy as np
import copy
from collections import OrderedDict


class StockBrokerage:
    def __init__(self, n_inputs, n_hidden, n_out, stock_names, num_brokers=100):
        self.brokers = [StockBroker(n_inputs, n_hidden, n_out, stock_names) for _ in range(num_brokers)]
        self.stock_names = stock_names

    def distribute_shares(self, all_stock_valuations, share_pool_size=1):
        '''
        Distributes shares to highest bidders according to *all_stock_valuations* parameter *share_pool_size* times
        for each type of stock.
        '''
        successful_transactions = [[] for _ in range(len(self.stock_names))]
        for i in range(share_pool_size):
            for stock_index in range(len(self.stock_names)):
                stock_valuations = [predictions[stock_index] for predictions in all_stock_valuations]
                if np.max(stock_valuations) <= 0:
                    break
                highest_bid = np.max(stock_valuations)
                highest_bidder = self.brokers[np.where(stock_valuations == highest_bid)[0][0]]
                if highest_bidder.funds > highest_bid:
                    successful_transactions[stock_index].append(highest_bid)
                    highest_bidder.funds -= highest_bid
                    highest_bidder.stocks[self.stock_names[stock_index]] += 1
                else:
                    stock_valuations[stock_valuations.index(highest_bid)] = 0
        return successful_transactions

    def distribute_money(self, funds):
        for broker in self.brokers:
            broker.funds += funds

    def yield_dividends(self, stock_name, payout):
        sum_of_stocks = sum([broker.stocks[stock_name] for broker in self.brokers])
        if sum_of_stocks > 0:
            payout_per_stock = payout / sum_of_stocks
            for broker in self.brokers:
                broker.dividends[stock_name] += broker.stocks[stock_name] * payout_per_stock

    def reset_broker_values(self):
        for broker in self.brokers:
            broker.funds = 0
            for key in broker.dividends.keys():
                broker.dividends[key] = 0
            for key in broker.stocks.keys():
                broker.stocks[key] = 0


class StockBroker:
    def __init__(self, input_size, num_neurons, num_predictions, stock_names, initial_mutations=3, initial_mutation_rate=1):
        self.dimensions = (input_size, num_neurons, num_predictions)
        self.layer1 = np.zeros((input_size + 1, num_neurons)) + (initial_mutations * initial_mutation_rate / ((input_size + 1) * num_neurons))
        self.layer2 = np.zeros((num_neurons + 1, num_predictions))+ (initial_mutations * initial_mutation_rate / ((num_neurons + 1) * num_predictions))
        for _ in range(initial_mutations):
            self.weighted_net_nudge_mutation(initial_mutation_rate)
        self.funds = 0.
        self.dividends = OrderedDict()
        for stock_name in stock_names:
            self.dividends[stock_name] = 0
        self.stocks = OrderedDict()
        for stock_name in stock_names:
            self.stocks[stock_name] = 0

    def predict(self, features):
        # A simple, shallow neural network forward pass with tanh non-linearity.
        inputs = np.pad(np.asarray(features), ((0, 0), (0, self.dimensions[0]+1-len(features[0]))), 'constant', constant_values=0)
        inputs[:, -1] = 0.5
        layer_1_activation = np.pad(np.tanh(np.matmul(inputs, self.layer1)), ((0, 0), (0, 1)), 'constant', constant_values=1)
        layer_2_activation = np.clip(np.matmul(layer_1_activation, self.layer2), 0, 1)
        return (layer_2_activation / (np.sum(layer_2_activation) + 0.001)) * self.funds

    def get_feature_state(self):
        # Provides information on the current state of investment scaled for use as network inputs.
        return [self.funds*0.001] + list([dividend*0.0001 for dividend in self.dividends.values()])

    def shuffle_neurons(self):
        # Reorders matrices while preserving prediction results by changing only the order of the hidden layer nodes.
        new_neuron_order = np.random.permutation(self.dimensions[1])
        self.layer1 = self.layer1[:, new_neuron_order]
        self.layer2[:-1, :] = self.layer2[:-1, :][new_neuron_order, :]

    def splice_with(self, other):
        '''
        Instantiates a new broker with the same total number of hidden nodes as this broker, which then copies a
        random combination of hidden layer nodes, and their associated layer weights from this broker, and the broker
        provided by the *other* parameter. The new broker has the same number of hidden nodes as this broker.
        '''
        self.shuffle_neurons()
        other.shuffle_neurons()
        cut_point = random.randrange(self.dimensions[1] - 1) + 1
        child_broker = copy.deepcopy(self)
        child_broker.layer1[:, :cut_point] = self.layer1[:, :cut_point]
        child_broker.layer1[:, cut_point:] = other.layer1[:, cut_point:]
        child_broker.layer2[:cut_point, :] = self.layer2[:cut_point, :]
        child_broker.layer2[cut_point:, :] = other.layer2[cut_point:, :]
        return child_broker

    @staticmethod
    def calculate_nudge_with_dimensions(dimensions, exponent=1000000000):
        # Generates weighted noise useful for diversity.
        random_nudge = np.random.rand(*dimensions)
        weighted_nudge = exponent ** random_nudge
        normalised_nudge = weighted_nudge / np.sum(weighted_nudge)
        return normalised_nudge

    def weighted_net_nudge_mutation(self, learning_rate):
        child_mutant = copy.deepcopy(self)
        child_mutant.layer1 += self.calculate_nudge_with_dimensions(child_mutant.layer1.shape) * learning_rate * random.random()
        child_mutant.layer1 -= self.calculate_nudge_with_dimensions(child_mutant.layer1.shape) * learning_rate * random.random()
        child_mutant.layer2 += self.calculate_nudge_with_dimensions(child_mutant.layer2.shape) * learning_rate * random.random()
        child_mutant.layer2 -= self.calculate_nudge_with_dimensions(child_mutant.layer2.shape) * learning_rate * random.random()
        return child_mutant

