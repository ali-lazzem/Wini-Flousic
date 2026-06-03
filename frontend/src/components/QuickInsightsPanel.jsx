const QuickInsightsPanel = ({ insights = {} }) => {
  const defaultInsights = {
    mostExpensive: 'Food',
    fastestGrowing: 'Transport',
    mostReduced: 'Snacks',
    averageDailySpending: 25,
    monthlyTrend: '+5%'
  };
  
  const data = { ...defaultInsights, ...insights };
  
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
      <div className="card p-3">
        <p className="text-xs text-gray-500 dark:text-gray-400">Most Expensive Category</p>
        <p className="font-bold text-gray-900 dark:text-white">{data.mostExpensive}</p>
      </div>
      <div className="card p-3">
        <p className="text-xs text-gray-500 dark:text-gray-400">Fastest Growing</p>
        <p className="font-bold text-red-500 dark:text-red-400">{data.fastestGrowing}</p>
      </div>
      <div className="card p-3">
        <p className="text-xs text-gray-500 dark:text-gray-400">Most Reduced</p>
        <p className="font-bold text-green-500 dark:text-green-400">{data.mostReduced}</p>
      </div>
      <div className="card p-3">
        <p className="text-xs text-gray-500 dark:text-gray-400">Avg Daily Spending</p>
        <p className="font-bold text-gray-900 dark:text-white">{data.averageDailySpending} TND</p>
      </div>
      <div className="card p-3">
        <p className="text-xs text-gray-500 dark:text-gray-400">Monthly Trend</p>
        <p className="font-bold text-blue-500 dark:text-blue-400">{data.monthlyTrend}</p>
      </div>
    </div>
  );
};

export default QuickInsightsPanel;