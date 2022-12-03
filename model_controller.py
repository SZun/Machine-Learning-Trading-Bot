import pandas as pd
import matplotlib.pyplot as plt

# Class to control all model-related interactions 
class Model_Controller:
    
    """
        Class to control all model-related interactions
    """
    
    # Constructor
    def __init__(self, model, model_name, data):
        
        """
            Class Constructor
            
            @Parameters: 
                - model: sklearn classifier
                - model_name: name of the sklearn model
                - data: dictionary with train & test data
        """
        
        # Setting all class variables
        self.model = model
        self.model_name = model_name
        self.X_train_scaled = data['X_train_scaled']
        self.X_test_scaled = data['X_test_scaled']
        self.X_test = data['X_test']
        self.y_train = data['y_train']
        self.y_test = data['y_test']
        self.signals_df = data['signals_df']
        self.pred = None
        self.df = None
        self.returns = 'Returns'
        self.actual_returns = 'Actual ' + self.returns
        self.strategy_returns = 'Strategy ' + self.returns
        # Setting predictions
        self.set_predictions()
        
    def set_predictions(self):
        
        """
            Instantiates the model, fits the model and sets the predictions.
        """
        
        self.pred = self.model(random_state=1).fit(self.X_train_scaled,self.y_train).predict(self.X_test_scaled)
        
    def get_predictions(self):
        
        """
            Returns the predictions
        """
        
        return self.pred
    
    def print_report(self):
        
        """
            Prints the classification report
        """
        
        print(self.y_test,self.pred)
        
    def get_df(self):
        
        """
            Creates and returns the predictions DataFrame
        """
        
        self.df = pd.DataFrame({'Predicted': self.pred, self.actual_returns: self.signals_df[self.actual_returns]}, index=self.X_test.index)
        self.df[self.strategy_returns] = self.df[self.actual_returns] * self.pred
        return self.df
    
    def display_head_tail(self):
        
        """
            Displays the head and tail of the predictions DataFrame
        """
        
        display(self.df.head(),self.df.tail())
        
    def plot_save_returns(self):
        
        """
            Plots the Actual Returns vs the Strategy Returns and saves the plot as an image
        """
        
        bold = 'bold'
        label_fontsize,ticks_fontsize = 18,14
        
        (1 + self.df[[self.actual_returns, self.strategy_returns]]).cumprod().plot(figsize=(20,10), linestyle=(0, (3, 1, 1, 1, 1, 1)));
        
        legend = plt.legend(title=self.returns, fontsize=12, loc=4)
        plt.setp(legend.get_title(),fontsize=16, fontweight=bold)
        
        plt.title(f'Actual vs {self.model_name} {self.strategy_returns} 2015-2020', fontsize=24, fontweight=bold)
        plt.grid(color='#eeeeee', linestyle='-', linewidth=1.25)
        plt.xlabel('Date', fontsize=label_fontsize, fontweight=bold)
        plt.ylabel(self.returns, fontsize=label_fontsize, fontweight=bold)
        plt.xticks(fontsize=ticks_fontsize,fontweight=bold)
        plt.yticks(fontsize=ticks_fontsize,fontweight=bold)
        
        plt.savefig(f'./assets/images/returns_{self.model_name}.png');