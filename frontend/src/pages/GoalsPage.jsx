import { useState, useEffect } from 'react';
import PageTransition from '../components/PageTransition';
import { goalApi } from '../services/api';
import DeleteConfirmModal from '../components/DeleteConfirmModal';
import { useToast } from '../hooks/useToast';
import ToastNotification from '../components/ToastNotification';
import AnimatedCounter from "../components/AnimatedCounter";

const GoalsPage = () => {
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingGoal, setEditingGoal] = useState(null);
  const [deleteModal, setDeleteModal] = useState({ open: false, id: null });
  const [form, setForm] = useState({ name: '', target_amount: '', deadline: '', category: '' });
  const { toast, showToast, hideToast } = useToast();

  useEffect(() => {
    fetchGoals();
  }, []);

  const fetchGoals = async () => {
    try {
      const res = await goalApi.list();
      setGoals(res.data);
    } catch (err) {
      showToast('Failed to load goals', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingGoal) {
        await goalApi.update(editingGoal.id, form);
        showToast('Goal updated');
      } else {
        await goalApi.create(form);
        showToast('Goal created');
      }
      setShowForm(false);
      setEditingGoal(null);
      setForm({ name: '', target_amount: '', deadline: '', category: '' });
      fetchGoals();
    } catch (err) {
      showToast('Error saving goal', 'error');
    }
  };

  const handleDelete = async () => {
    try {
      await goalApi.delete(deleteModal.id);
      showToast('Goal deleted');
      fetchGoals();
    } catch (err) {
      showToast('Delete failed', 'error');
    } finally {
      setDeleteModal({ open: false, id: null });
    }
  };

  const startEdit = (goal) => {
    setEditingGoal(goal);
    setForm({
      name: goal.name,
      target_amount: goal.target_amount,
      deadline: goal.deadline,
      category: goal.category || '',
    });
    setShowForm(true);
  };

  return (
    <PageTransition>
      <div className="p-6 space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Financial Goals</h1>
          <button
            onClick={() => { setEditingGoal(null); setForm({ name: '', target_amount: '', deadline: '', category: '' }); setShowForm(true); }}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
          >
            + New Goal
          </button>
        </div>

        {showForm && (
          <div className="card p-6">
            <h2 className="text-xl font-semibold mb-4">{editingGoal ? 'Edit Goal' : 'Create Goal'}</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <input type="text" placeholder="Goal name (e.g., New Laptop)" value={form.name} onChange={e => setForm({...form, name: e.target.value})} required className="w-full p-2 border rounded dark:bg-gray-800" />
              <input type="number" step="0.01" placeholder="Target amount (TND)" value={form.target_amount} onChange={e => setForm({...form, target_amount: e.target.value})} required className="w-full p-2 border rounded dark:bg-gray-800" />
              <input type="date" placeholder="Deadline" value={form.deadline} onChange={e => setForm({...form, deadline: e.target.value})} required className="w-full p-2 border rounded dark:bg-gray-800" />
              <select value={form.category} onChange={e => setForm({...form, category: e.target.value})} className="w-full p-2 border rounded dark:bg-gray-800">
                <option value="">All categories (optional)</option>
                <option value="food">Food</option><option value="drinks">Drinks</option><option value="transport">Transport</option>
                <option value="fun">Fun</option><option value="university">University</option><option value="groceries">Groceries</option>
                <option value="snacks">Snacks</option><option value="others">Others</option>
              </select>
              <div className="flex space-x-3">
                <button type="submit" className="bg-green-600 text-white px-4 py-2 rounded-lg">Save</button>
                <button type="button" onClick={() => setShowForm(false)} className="bg-gray-500 text-white px-4 py-2 rounded-lg">Cancel</button>
              </div>
            </form>
          </div>
        )}

        {loading ? (
          <div className="text-center text-gray-500">Loading goals...</div>
        ) : goals.length === 0 ? (
          <div className="card p-8 text-center text-gray-500">No goals yet. Create your first financial goal!</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {goals.map(goal => (
              <div key={goal.id} className="card p-4 hover:shadow-lg transition">
                <div className="flex justify-between items-start">
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white">{goal.name}</h3>
                  <div className="flex space-x-2">
                    <button onClick={() => startEdit(goal)} className="text-blue-600 dark:text-blue-400">✏️</button>
                    <button onClick={() => setDeleteModal({ open: true, id: goal.id })} className="text-red-600 dark:text-red-400">🗑️</button>
                  </div>
                </div>
<p className="text-sm text-gray-500 dark:text-gray-400">Target: <AnimatedCounter value={goal.target_amount} suffix=" TND" /></p>
<p className="text-sm text-gray-500 dark:text-gray-400">Current: <AnimatedCounter value={goal.current_amount} suffix=" TND" /></p>
                <div className="mt-2 h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div className="h-full bg-green-500 rounded-full" style={{ width: `${goal.progress_percent}%` }}></div>
                </div>
                <p className="text-xs text-right mt-1">{goal.progress_percent.toFixed(0)}%</p>
                <p className="text-xs text-gray-400 mt-2">Deadline: {goal.deadline}</p>
              </div>
            ))}
          </div>
        )}

        <DeleteConfirmModal
          isOpen={deleteModal.open}
          onClose={() => setDeleteModal({ open: false, id: null })}
          onConfirm={handleDelete}
          title="Delete Goal"
          message="Are you sure you want to delete this goal?"
        />
        {toast && <ToastNotification message={toast.message} type={toast.type} onClose={hideToast} />}
      </div>
    </PageTransition>
  );
};

export default GoalsPage;