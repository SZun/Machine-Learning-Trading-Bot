import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report

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
        
        # Calling method to set predictions
        self.set_predictions()
        
        # Method to set predictions
    def set_predictions(self):
        
        """
            Instantiates the model, fits the model and sets the predictions.
        """
        # Setting predictions
        self.pred = self.model(random_state=1).fit(self.X_train_scaled,self.y_train).predict(self.X_test_scaled)
        
        # Method to get predictions
    def get_predictions(self):
        
        """
            Returns the predictions
        """
        # Returning predictions
        return self.pred
    
        # Method to print classifica
    def print_report(self):
        
        """
            Prints the classification report
        """
        
        # Printing classification report
        print(classification_report(self.y_test,self.pred))
        
        # Method to get predictions DataFrame
    def get_df(self):
        
        """
            Creates and returns the predictions DataFrame
        """
        # Intializing the DataFrame with predicted column/data, actual returns column/data and index
        self.df = pd.DataFrame({'Predicted': self.pred, self.actual_returns: self.signals_df[self.actual_returns]}, index=self.X_test.index)
        
        # Setting the strategy returns column
        self.df[self.strategy_returns] = self.df[self.actual_returns] * self.pred
        
        # Returning the DataFrame
        return self.df
    
        # Method to display the head and tail of the DataFrame
    def display_head_tail(self):
        
        """
            Displays the head and tail of the predictions DataFrame
        """
        # Displaying the head and tail of the DataFrame
        display(self.df.head(),self.df.tail())
        
        # Method to plot the returns and save the plot as an image
    def plot_save_returns(self):
        
        """
            Plots the Actual Returns vs the Strategy Returns and saves the plot as an image
        """
        
        # Setting the fontweight variable
        bold = 'bold'
        # Setting the fontsize variable
        label_fontsize,ticks_fontsize = 18,14
        
        # Plotting the cumulative actual vs strategy returns 
        (1 + self.df[[self.actual_returns, self.strategy_returns]]).cumprod().plot(
            figsize=(20,10),
            linewidth=3,
            color=['#00FFEF','#FFD700'],
            marker='X',
            markersize=6,
            markerfacecolor='#000000',
            linestyle=(0,(1,1))
        );
        
        # Setting the legend
        legend = plt.legend(title=self.returns, fontsize=12, loc=4)
        # Changing the style of the legend title
        plt.setp(legend.get_title(),fontsize=16, fontweight=bold)
        
        # Setting the title
        plt.title(f'Actual vs {self.model_name} Strategy Cumulative {self.returns} 2015-2021', fontsize=24, fontweight=bold)
        # Setting the grid
        plt.grid(color='#eeeeee', linestyle='-', linewidth=1.25)
        # Setting the X & Y labels
        plt.xlabel('Date', fontsize=label_fontsize, fontweight=bold)
        plt.ylabel(self.returns, fontsize=label_fontsize, fontweight=bold)
        # Styling the X & Y ticks
        plt.xticks(fontsize=ticks_fontsize,fontweight=bold)
        plt.yticks(fontsize=ticks_fontsize,fontweight=bold)
        
        # Saving the plot
        plt.savefig(f'./assets/images/returns_{self.model_name}.png');