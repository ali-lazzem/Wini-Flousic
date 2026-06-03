import { useState, useEffect } from 'react';
import PageTransition from '../components/PageTransition';
import api from '../services/api';
import { usePagination } from '../hooks/usePagination';

const TransactionsPage = () => {
  const [transactions, setTransactions] = useState([]);
  const [filteredTransactions, setFilteredTransactions] = useState([]);
  const [form, setForm] = useState({
    type: 'expense',
    amount: '',
    description: '',
    date: new Date().toISOString().slice(0, 10),
    payment_method: 'cash',
    category: ''
  });
  const [filters, setFilters] = useState({
    type: '',
    category: '',
    payment_method: '',
    startDate: '',
    endDate: '',
    search: ''
  });
  const { paginatedItems, currentPage, totalPages, nextPage, prevPage, hasNextPage, hasPrevPage } =
    usePagination(filteredTransactions, 10);
  const [exporting, setExporting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      const res = await api.get('transactions/');
      setTransactions(res.data);
      applyFilters(res.data);
      setError('');
    } catch (err) {
      console.error(err);
      setError('Failed to load transactions');
    }
  };

  const applyFilters = (data = transactions) => {
    let filtered = [...data];
    if (filters.type) filtered = filtered.filter(t => t.type === filters.type);
    if (filters.category) filtered = filtered.filter(t => t.category === filters.category);
    if (filters.payment_method) filtered = filtered.filter(t => t.payment_method === filters.payment_method);
    if (filters.startDate) filtered = filtered.filter(t => t.date >= filters.startDate);
    if (filters.endDate) filtered = filtered.filter(t => t.date <= filters.endDate);
    if (filters.search) filtered = filtered.filter(t => t.description?.toLowerCase().includes(filters.search.toLowerCase()));
    setFilteredTransactions(filtered);
  };

  useEffect(() => {
    applyFilters();
  }, [filters, transactions]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await api.post('transactions/', form);
      fetchTransactions();
      setForm({ ...form, amount: '', description: '', category: '' });
    } catch (err) {
      console.error(err);
      const errorMsg = err.response?.data?.detail || 'Failed to add transaction';
      setError(errorMsg);
      // Auto-clear error after 5 seconds
      setTimeout(() => setError(''), 5000);
    }
  };

  const handleExport = async () => {
    setExporting(true);
    try {
      const response = await api.get('transactions/export/', {
        responseType: 'blob',
      });
      const blob = new Blob([response.data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'transactions.csv');
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      setError('');
    } catch (err) {
      console.error('Export failed:', err);
      setError('Failed to export transactions');
      setTimeout(() => setError(''), 5000);
    } finally {
      setExporting(false);
    }
  };

  return (
    <PageTransition>
      <div className="p-6 space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Transactions</h1>
          <button
            onClick={handleExport}
            disabled={exporting}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50"
          >
            {exporting ? 'Exporting...' : 'Export CSV'}
          </button>
        </div>

        {error && (
          <div className="bg-red-100 dark:bg-red-900/30 border border-red-400 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        <div className="card p-4">
          <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Add New Transaction</h2>
          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <select
              value={form.type}
              onChange={e => setForm({ ...form, type: e.target.value })}
              className="bg-gray-50 dark:bg-gray-800 border rounded-md px-3 py-2"
            >
              <option value="expense">Expense</option>
              <option value="income">Income</option>
            </select>
            {form.type === 'expense' && (
              <select
                value={form.category}
                onChange={e => setForm({ ...form, category: e.target.value })}
                required
                className="bg-gray-50 dark:bg-gray-800 border rounded-md px-3 py-2"
              >
                <option value="">Category</option>
                <option value="food">Food</option>
                <option value="drinks">Drinks</option>
                <option value="transport">Transport</option>
                <option value="fun">Fun</option>
                <option value="university">University</option>
                <option value="groceries">Groceries</option>
                <option value="snacks">Snacks</option>
                <option value="others">Others</option>
              </select>
            )}
            <input
              type="number"
              step="0.01"
              placeholder="Amount"
              value={form.amount}
              onChange={e => setForm({ ...form, amount: e.target.value })}
              required
              className="bg-gray-50 dark:bg-gray-800 border rounded-md px-3 py-2"
            />
            <input
              type="text"
              placeholder="Description"
              value={form.description}
              onChange={e => setForm({ ...form, description: e.target.value })}
              className="bg-gray-50 dark:bg-gray-800 border rounded-md px-3 py-2"
            />
            <input
              type="date"
              value={form.date}
              onChange={e => setForm({ ...form, date: e.target.value })}
              className="bg-gray-50 dark:bg-gray-800 border rounded-md px-3 py-2"
            />
            <select
              value={form.payment_method}
              onChange={e => setForm({ ...form, payment_method: e.target.value })}
              className="bg-gray-50 dark:bg-gray-800 border rounded-md px-3 py-2"
            >
              <option value="cash">Cash</option>
              <option value="bank">Bank Account</option>
            </select>
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md transition"
            >
              Add Transaction
            </button>
          </form>
        </div>

        <div className="card p-4">
          <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Filters</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <select
              value={filters.type}
              onChange={e => setFilters({ ...filters, type: e.target.value })}
              className="bg-gray-50 dark:bg-gray-800 border rounded-md px-3 py-2"
            >
              <option value="">All Types</option>
              <option value="income">Income</option>
              <option value="expense">Expense</option>
            </select>
            <select
              value={filters.category}
              onChange={e => setFilters({ ...filters, category: e.target.value })}
              className="bg-gray-50 dark:bg-gray-800 border rounded-md px-3 py-2"
            >
              <option value="">All Categories</option>
              <option value="food">Food</option>
              <option value="drinks">Drinks</option>
              <option value="transport">Transport</option>
              <option value="fun">Fun</option>
              <option value="university">University</option>
              <option value="groceries">Groceries</option>
              <option value="snacks">Snacks</option>
              <option value="others">Others</option>
            </select>
            <select
              value={filters.payment_method}
              onChange={e => setFilters({ ...filters, payment_method: e.target.value })}
              className="bg-gray-50 dark:bg-gray-800 border rounded-md px-3 py-2"
            >
              <option value="">All Methods</option>
              <option value="cash">Cash</option>
              <option value="bank">Bank</option>
            </select>
            <input
              type="date"
              placeholder="Start Date"
              value={filters.startDate}
              onChange={e => setFilters({ ...filters, startDate: e.target.value })}
              className="bg-gray-50 dark:bg-gray-800 border rounded-md px-3 py-2"
            />
            <input
              type="date"
              placeholder="End Date"
              value={filters.endDate}
              onChange={e => setFilters({ ...filters, endDate: e.target.value })}
              className="bg-gray-50 dark:bg-gray-800 border rounded-md px-3 py-2"
            />
            <input
              type="text"
              placeholder="Search description"
              value={filters.search}
              onChange={e => setFilters({ ...filters, search: e.target.value })}
              className="bg-gray-50 dark:bg-gray-800 border rounded-md px-3 py-2"
            />
          </div>
        </div>

        <div className="card p-4 overflow-x-auto">
          <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Transaction History</h2>
          <table className="min-w-full text-sm">
            <thead className="bg-gray-100 dark:bg-gray-800">
              <tr>
                <th className="p-2">Type</th>
                <th className="p-2">Category</th>
                <th className="p-2">Amount</th>
                <th className="p-2">Date</th>
                <th className="p-2">Method</th>
                <th className="p-2">Description</th>
              </tr>
            </thead>
            <tbody>
              {paginatedItems.map(tx => (
                <tr key={tx.id} className="border-b border-gray-200 dark:border-gray-700">
                  <td className="p-2 capitalize text-gray-900 dark:text-white">{tx.type}</td>
                  <td className="p-2 capitalize text-gray-900 dark:text-white">{tx.category || '-'}</td>
                  <td className="p-2 text-gray-900 dark:text-white">{tx.amount} TND</td>
                  <td className="p-2 text-gray-600 dark:text-gray-400">{tx.date}</td>
                  <td className="p-2 capitalize text-gray-600 dark:text-gray-400">{tx.payment_method}</td>
                  <td className="p-2 text-gray-600 dark:text-gray-400">{tx.description || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="flex justify-between items-center mt-4">
            <button
              onClick={prevPage}
              disabled={!hasPrevPage}
              className="px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded disabled:opacity-50"
            >
              Previous
            </button>
            <span>
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={nextPage}
              disabled={!hasNextPage}
              className="px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </PageTransition>
  );
};

export default TransactionsPage;