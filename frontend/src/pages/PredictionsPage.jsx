import { useEffect, useState } from 'react';
import api from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';

const PredictionsPage = () => {
  const [data, setData] = useState(null);
  const [aiInsights, setAiInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        const [forecastRes, insightsRes] = await Promise.all([
          api.get('predictions/expense-forecast/'),
          api.get('predictions/ai-insights/')
        ]);
        setData(forecastRes.data);
        setAiInsights(insightsRes.data);
        setError(null);
      } catch (err) {
        console.error(err);
        setError('Failed to load predictions');
      } finally {
        setLoading(false);
      }
    };
    fetchPredictions();
  }, []);

  if (loading) return <div className="p-6 text-center">Loading AI predictions...</div>;
  if (error) return <div className="p-6 text-red-600">{error}</div>;

  const chartData = data?.historical_expenses?.map((val, idx) => ({ month: `Month ${idx+1}`, historical: val, predicted: null })) || [];
  if (data?.predicted_expense_next_month) {
    chartData.push({ month: 'Next Month', historical: null, predicted: data.predicted_expense_next_month });
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white">AI Financial Predictions</h1>

      {/* Forecast Chart */}
      <div className="card p-6">
        <h2 className="text-xl font-semibold mb-4">Expense Forecast</h2>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip formatter={(val) => `${val?.toFixed(2)} TND`} />
            <Legend />
            <Line type="monotone" dataKey="historical" stroke="#3b82f6" name="Historical" />
            <Line type="monotone" dataKey="predicted" stroke="#10b981" name="Predicted" strokeDasharray="5 5" />
            <ReferenceLine x="Next Month" stroke="#ef4444" label="Forecast Start" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* AI Insights */}
      <div className="card p-6">
        <h2 className="text-xl font-semibold mb-4">AI Insights & Recommendations</h2>
        <div className="space-y-4">
          <div><strong>Budget Recommendation:</strong> {aiInsights?.budget_recommendation}</div>
          <div><strong>Savings Forecast:</strong> {aiInsights?.savings_forecast} TND next month</div>
          <div><strong>Category Trends:</strong>
            <ul className="list-disc pl-5 mt-2">
              {aiInsights?.category_trends?.slice(0,5).map((trend, i) => <li key={i}>{trend.insight}</li>)}
            </ul>
          </div>
          <div><strong>Recurring Expenses:</strong>
            <ul className="list-disc pl-5 mt-2">
              {aiInsights?.recurring_expenses?.map((exp, i) => <li key={i}>{exp.category}: ~{exp.average_amount} TND/month</li>)}
            </ul>
          </div>
          <div><strong>Overspending Alerts:</strong>
            <ul className="list-disc pl-5 mt-2 text-red-600">
              {aiInsights?.overspending_alerts?.map((alert, i) => <li key={i}>{alert}</li>)}
            </ul>
          </div>
        </div>
      </div>

      {/* Risk Score Card */}
      <div className={`rounded-lg p-6 ${data?.risk_score > 0.3 ? 'bg-yellow-50 dark:bg-yellow-900/20' : 'bg-green-50 dark:bg-green-900/20'}`}>
        <p className="font-bold">Risk Score: {(data?.risk_score * 100).toFixed(0)}%</p>
        <p>{data?.recommendation}</p>
      </div>
    </div>
  );
};

export default PredictionsPage;