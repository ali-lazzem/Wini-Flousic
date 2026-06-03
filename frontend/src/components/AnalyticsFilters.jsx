import { useState } from 'react';

const AnalyticsFilters = ({ onChange, initialFilters = {} }) => {
  const [filters, setFilters] = useState({
    startDate: initialFilters.startDate || '',
    endDate: initialFilters.endDate || '',
    category: initialFilters.category || '',
    paymentMethod: initialFilters.paymentMethod || 'all'
  });
  
  const handleChange = (e) => {
    const newFilters = { ...filters, [e.target.name]: e.target.value };
    setFilters(newFilters);
    if (onChange) onChange(newFilters);
  };
  
  return (
    <div className="card p-4 mb-6">
      <div className="flex flex-wrap gap-4 items-end">
        <div>
          <label className="block text-sm text-gray-600 dark:text-gray-400">Start Date</label>
          <input type="date" name="startDate" value={filters.startDate} onChange={handleChange}
            className="mt-1 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 text-gray-900 dark:text-white rounded-md px-3 py-1" />
        </div>
        <div>
          <label className="block text-sm text-gray-600 dark:text-gray-400">End Date</label>
          <input type="date" name="endDate" value={filters.endDate} onChange={handleChange}
            className="mt-1 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 text-gray-900 dark:text-white rounded-md px-3 py-1" />
        </div>
        <div>
          <label className="block text-sm text-gray-600 dark:text-gray-400">Category</label>
          <select name="category" value={filters.category} onChange={handleChange}
            className="mt-1 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 text-gray-900 dark:text-white rounded-md px-3 py-1">
            <option value="">All</option>
            <option value="food">Food</option>
            <option value="drinks">Drinks</option>
            <option value="transport">Transport</option>
            <option value="fun">Fun</option>
            <option value="university">University</option>
            <option value="groceries">Groceries</option>
            <option value="snacks">Snacks</option>
            <option value="others">Others</option>
          </select>
        </div>
        <div>
          <label className="block text-sm text-gray-600 dark:text-gray-400">Payment Method</label>
          <select name="paymentMethod" value={filters.paymentMethod} onChange={handleChange}
            className="mt-1 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 text-gray-900 dark:text-white rounded-md px-3 py-1">
            <option value="all">All</option>
            <option value="cash">Cash</option>
            <option value="bank">Bank</option>
          </select>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsFilters;