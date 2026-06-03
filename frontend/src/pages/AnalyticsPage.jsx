import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  PieChart, Pie, Cell, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip,
  Legend, LineChart, Line, ResponsiveContainer
} from 'recharts';
import PageTransition from '../components/PageTransition';
import AnimatedCounter from '../components/AnimatedCounter';
import api from '../services/api';

const container = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.1 } }
};
const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

const DashboardPage = () => {
  const [stats, setStats] = useState({
    cashBalance: 0,
    bankBalance: 0,
    monthlyIncome: 0,
    monthlyExpenses: 0,
    monthlySavings: 0,
    netCashflow: 0,
    avgDailySpending: 0,
    largestExpense: 0,
    prevMonthIncome: 0,
    prevMonthExpenses: 0,
    prevMonthSavings: 0,
    topCategories: [],
    recentTransactions: [],
    monthlyTrend: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [quickFilter, setQuickFilter] = useState('this_month');

  useEffect(() => {
    const fetchDashboard = async () => {
      setLoading(true);
      try {
        const res = await api.get(`transactions/dashboard/?period=${quickFilter}`);
        console.log('API Response:', res.data); // Debug log
        // Safely extract arrays, defaulting to empty array if missing
        const safeData = {
          cashBalance: res.data.cashBalance ?? 0,
          bankBalance: res.data.bankBalance ?? 0,
          monthlyIncome: res.data.monthlyIncome ?? 0,
          monthlyExpenses: res.data.monthlyExpenses ?? 0,
          monthlySavings: res.data.monthlySavings ?? 0,
          netCashflow: res.data.netCashflow ?? 0,
          avgDailySpending: res.data.avgDailySpending ?? 0,
          largestExpense: res.data.largestExpense ?? 0,
          prevMonthIncome: res.data.prevMonthIncome ?? 0,
          prevMonthExpenses: res.data.prevMonthExpenses ?? 0,
          prevMonthSavings: res.data.prevMonthSavings ?? 0,
          topCategories: Array.isArray(res.data.topCategories) ? res.data.topCategories : [],
          recentTransactions: Array.isArray(res.data.recentTransactions) ? res.data.recentTransactions : [],
          monthlyTrend: Array.isArray(res.data.monthlyTrend) ? res.data.monthlyTrend : []
        };
        setStats(safeData);
        setError(null);
      } catch (err) {
        console.error('Dashboard error:', err);
        setError(err.response?.data?.error || 'Failed to load dashboard data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, [quickFilter]);

  if (loading) {
    return <div className="flex justify-center items-center h-64"><div className="text-gray-600 dark:text-gray-400">Loading dashboard...</div></div>;
  }

  if (error) {
    return (
      <div className="p-6 text-center">
        <div className="bg-red-100 dark:bg-red-900/30 border border-red-400 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg">
          <p>{error}</p>
          <button onClick={() => window.location.reload()} className="mt-2 bg-red-600 text-white px-3 py-1 rounded">Retry</button>
        </div>
      </div>
    );
  }

  const categoryColors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#ec489a', '#14b8a6', '#f97316'];

  const barData = [
    { name: 'Income', amount: stats.monthlyIncome, fill: '#10b981' },
    { name: 'Expenses', amount: stats.monthlyExpenses, fill: '#ef4444' }
  ];

  const balanceData = [
    { name: 'Cash', value: stats.cashBalance, fill: '#3b82f6' },
    { name: 'Bank', value: stats.bankBalance, fill: '#8b5cf6' }
  ];

  return (
    <PageTransition>
      <div className="p-4 md:p-6 space-y-6">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
          <div className="flex flex-wrap gap-2">
            <button onClick={() => setQuickFilter('this_month')} className={`px-3 py-1 rounded-md text-sm ${quickFilter === 'this_month' ? 'bg-green-600 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'}`}>This Month</button>
            <button onClick={() => setQuickFilter('last_month')} className={`px-3 py-1 rounded-md text-sm ${quickFilter === 'last_month' ? 'bg-green-600 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'}`}>Last Month</button>
            <button onClick={() => setQuickFilter('last_3')} className={`px-3 py-1 rounded-md text-sm ${quickFilter === 'last_3' ? 'bg-green-600 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'}`}>Last 3 Months</button>
            <button onClick={() => setQuickFilter('last_6')} className={`px-3 py-1 rounded-md text-sm ${quickFilter === 'last_6' ? 'bg-green-600 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'}`}>Last 6 Months</button>
            <button onClick={() => setQuickFilter('this_year')} className={`px-3 py-1 rounded-md text-sm ${quickFilter === 'this_year' ? 'bg-green-600 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'}`}>This Year</button>
          </div>
        </div>

        <motion.div variants={container} initial="hidden" animate="show" className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <motion.div variants={item} className="card p-4 hover:shadow-lg transition">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Monthly Income</h3>
            <p className="text-2xl font-bold text-green-600 dark:text-green-400"><AnimatedCounter value={stats.monthlyIncome} suffix=" TND" /></p>
            <p className="text-xs text-gray-400">vs last month: {stats.prevMonthIncome > 0 ? `${((stats.monthlyIncome - stats.prevMonthIncome) / stats.prevMonthIncome * 100).toFixed(1)}%` : '—'}</p>
          </motion.div>
          <motion.div variants={item} className="card p-4 hover:shadow-lg transition">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Monthly Expenses</h3>
            <p className="text-2xl font-bold text-red-600 dark:text-red-400"><AnimatedCounter value={stats.monthlyExpenses} suffix=" TND" /></p>
            <p className="text-xs text-gray-400">vs last month: {stats.prevMonthExpenses > 0 ? `${((stats.monthlyExpenses - stats.prevMonthExpenses) / stats.prevMonthExpenses * 100).toFixed(1)}%` : '—'}</p>
          </motion.div>
          <motion.div variants={item} className="card p-4 hover:shadow-lg transition">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Monthly Savings</h3>
            <p className={`text-2xl font-bold ${stats.monthlySavings >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}><AnimatedCounter value={stats.monthlySavings} suffix=" TND" /></p>
          </motion.div>
          <motion.div variants={item} className="card p-4 hover:shadow-lg transition">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Avg Daily Spending</h3>
            <p className="text-2xl font-bold text-gray-900 dark:text-white"><AnimatedCounter value={stats.avgDailySpending} suffix=" TND" /></p>
          </motion.div>
          <motion.div variants={item} className="card p-4 hover:shadow-lg transition">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Largest Expense</h3>
            <p className="text-2xl font-bold text-gray-900 dark:text-white"><AnimatedCounter value={stats.largestExpense} suffix=" TND" /></p>
          </motion.div>
          <motion.div variants={item} className="card p-4 hover:shadow-lg transition">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Net Cash Flow</h3>
            <p className="text-2xl font-bold text-blue-600 dark:text-blue-400"><AnimatedCounter value={stats.netCashflow} suffix=" TND" /></p>
          </motion.div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="card p-4">
            <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Spending by Category</h3>
            {stats.topCategories.length === 0 ? (
              <p className="text-gray-500">No spending data yet.</p>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie data={stats.topCategories} dataKey="total" nameKey="category" cx="50%" cy="50%" outerRadius={100} label>
                    {stats.topCategories.map((entry, idx) => <Cell key={`cell-${idx}`} fill={categoryColors[idx % categoryColors.length]} />)}
                  </Pie>
                  <Tooltip formatter={(val) => `${val} TND`} />
                </PieChart>
              </ResponsiveContainer>
            )}
          </div>
          <div className="card p-4">
            <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Income vs Expenses</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip formatter={(val) => `${val} TND`} />
                <Bar dataKey="amount" fill="#10b981" />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="card p-4">
            <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Monthly Trend</h3>
            {stats.monthlyTrend.length === 0 ? (
              <p className="text-gray-500">Not enough historical data.</p>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={stats.monthlyTrend}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip formatter={(val) => `${val} TND`} />
                  <Legend />
                  <Line type="monotone" dataKey="income" stroke="#10b981" name="Income" />
                  <Line type="monotone" dataKey="expense" stroke="#ef4444" name="Expense" />
                  <Line type="monotone" dataKey="savings" stroke="#f59e0b" name="Savings" />
                </LineChart>
              </ResponsiveContainer>
            )}
          </div>
          <div className="card p-4">
            <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Cash vs Bank Balance</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie data={balanceData} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={60} outerRadius={100} label>
                  <Cell fill="#3b82f6" /><Cell fill="#8b5cf6" />
                </Pie>
                <Tooltip formatter={(val) => `${val} TND`} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="card p-4">
            <h3 className="text-lg font-semibold mb-3 text-gray-900 dark:text-white">Recent Transactions</h3>
            {stats.recentTransactions.length === 0 ? (
              <p className="text-gray-500">No recent transactions.</p>
            ) : (
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {stats.recentTransactions.map(tx => (
                  <div key={tx.id} className="flex justify-between border-b border-gray-200 dark:border-gray-700 py-2">
                    <span className="text-sm text-gray-600 dark:text-gray-400">{tx.description || tx.category}</span>
                    <span className={`text-sm font-medium ${tx.type === 'expense' ? 'text-red-600' : 'text-green-600'}`}>{tx.amount} TND</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </PageTransition>
  );
};

export default DashboardPage;