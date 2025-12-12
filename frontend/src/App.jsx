import React, { useState, useEffect } from 'react';
import { 
  Layout, 
  Plus, 
  Trash2, 
  Users, 
  FileText, 
  CheckCircle, 
  XCircle, 
  HelpCircle,
  Settings,
  LogOut,
  Play
} from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000';

// --- UI Components ---

const Card = ({ children, className = "" }) => (
  <div className={`bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden ${className}`}>
    {children}
  </div>
);

const Button = ({ children, onClick, variant = 'primary', className = "", type = "button", disabled = false }) => {
  const baseStyle = "px-4 py-2 rounded-lg font-bold transition-all transform active:scale-95 flex items-center justify-center gap-2";
  const variants = {
    primary: "bg-indigo-600 text-white hover:bg-indigo-700 shadow-md shadow-indigo-200",
    secondary: "bg-slate-100 text-slate-700 hover:bg-slate-200",
    danger: "bg-red-100 text-red-600 hover:bg-red-200",
    success: "bg-green-600 text-white hover:bg-green-700 shadow-md shadow-green-200",
    outline: "border-2 border-slate-200 text-slate-600 hover:border-indigo-600 hover:text-indigo-600"
  };

  return (
    <button 
      type={type} 
      onClick={onClick} 
      disabled={disabled}
      className={`${baseStyle} ${variants[variant]} ${disabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}
    >
      {children}
    </button>
  );
};

const Input = ({ label, type = "text", value, onChange, placeholder, required = false }) => (
  <div className="mb-4">
    {label && <label className="block text-sm font-semibold text-slate-700 mb-1">{label}</label>}
    <input
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      required={required}
      className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
    />
  </div>
);

const Select = ({ label, value, onChange, options }) => (
  <div className="mb-4">
    {label && <label className="block text-sm font-semibold text-slate-700 mb-1">{label}</label>}
    <select
      value={value}
      onChange={onChange}
      className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all bg-white"
    >
      {options.map((opt) => (
        <option key={opt.value} value={opt.value}>
          {opt.label}
        </option>
      ))}
    </select>
  </div>
);

const Badge = ({ children, color = "blue" }) => {
  const colors = {
    blue: "bg-blue-100 text-blue-700",
    green: "bg-green-100 text-green-700",
    purple: "bg-purple-100 text-purple-700",
  };
  return (
    <span className={`px-2 py-0.5 rounded-full text-xs font-bold uppercase tracking-wide ${colors[color] || colors.blue}`}>
      {children}
    </span>
  );
};

// --- Main App Component ---

export default function App() {
  const [currentView, setCurrentView] = useState('dashboard'); // dashboard, create-kahoot, users, kahoot-details
  const [kahoots, setKahoots] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedKahoot, setSelectedKahoot] = useState(null);

  // --- Fetch Data ---

  const fetchKahoots = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/all_kahoots`);
      if (!response.ok) throw new Error('Failed to fetch kahoots');
      const data = await response.json();
      setKahoots(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
      setError("Could not load Kahoots. Is the backend running on port 8000?");
    } finally {
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/all_users`);
      if (!response.ok) throw new Error('Failed to fetch users');
      const data = await response.json();
      setUsers(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
      setError("Could not load Users.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (currentView === 'dashboard') fetchKahoots();
    if (currentView === 'users') fetchUsers();
  }, [currentView]);

  // --- Actions ---

  const handleDeleteKahoot = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm("Are you sure you want to delete this Kahoot?")) return;
    
    try {
      const response = await fetch(`${API_BASE_URL}/your_kahoot/${id}`, { method: 'DELETE' });
      if (response.ok) {
        setKahoots(kahoots.filter(k => k.id !== id));
      } else {
        alert("Failed to delete Kahoot");
      }
    } catch (err) {
      alert("Error deleting Kahoot");
    }
  };

  const handleDeleteUser = async (username) => {
    if (!window.confirm(`Delete user ${username}?`)) return;

    try {
      const response = await fetch(`${API_BASE_URL}/users/${username}`, { method: 'DELETE' });
      if (response.ok) {
        setUsers(users.filter(u => u.username !== username));
      } else {
        alert("Failed to delete user");
      }
    } catch (err) {
      alert("Error deleting user");
    }
  };

  // --- Views ---

  const Sidebar = () => (
    <div className="w-64 bg-white border-r border-slate-200 flex flex-col h-screen fixed left-0 top-0 z-10">
      <div className="p-6 border-b border-slate-100 flex items-center gap-2">
        <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
          <span className="text-white font-bold text-lg">K!</span>
        </div>
        <span className="text-xl font-black text-slate-800 tracking-tight">KahootClone</span>
      </div>
      
      <nav className="flex-1 p-4 space-y-2">
        <SidebarItem 
          icon={<Layout size={20} />} 
          label="Kahoots" 
          active={currentView === 'dashboard'} 
          onClick={() => setCurrentView('dashboard')} 
        />
        <SidebarItem 
          icon={<Plus size={20} />} 
          label="Create Kahoot" 
          active={currentView === 'create-kahoot'} 
          onClick={() => setCurrentView('create-kahoot')} 
        />
        <SidebarItem 
          icon={<Users size={20} />} 
          label="Users" 
          active={currentView === 'users'} 
          onClick={() => setCurrentView('users')} 
        />
      </nav>

      <div className="p-4 border-t border-slate-100">
        <div className="flex items-center gap-3 p-2 rounded-lg bg-slate-50">
          <div className="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-bold">
            A
          </div>
          <div className="text-sm">
            <p className="font-bold text-slate-700">Admin</p>
            <p className="text-slate-500 text-xs">admin@kahoot.clone</p>
          </div>
        </div>
      </div>
    </div>
  );

  const SidebarItem = ({ icon, label, active, onClick }) => (
    <button 
      onClick={onClick}
      className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-bold transition-colors ${
        active 
          ? 'bg-indigo-50 text-indigo-600' 
          : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
      }`}
    >
      {icon}
      {label}
    </button>
  );

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 pl-64">
      <Sidebar />
      
      <main className="p-8 max-w-7xl mx-auto">
        {/* Error Banner */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
            <XCircle size={20} />
            {error}
            <button onClick={() => setError(null)} className="ml-auto text-sm font-bold hover:underline">Dismiss</button>
          </div>
        )}

        {currentView === 'dashboard' && (
          <DashboardView 
            kahoots={kahoots} 
            loading={loading} 
            onDelete={handleDeleteKahoot}
            onSelect={(k) => {
              setSelectedKahoot(k);
              setCurrentView('kahoot-details');
            }}
          />
        )}

        {currentView === 'create-kahoot' && (
          <CreateKahootView 
            onSuccess={() => setCurrentView('dashboard')}
            onCancel={() => setCurrentView('dashboard')}
          />
        )}

        {currentView === 'users' && (
          <UsersView 
            users={users} 
            loading={loading}
            onDelete={handleDeleteUser}
            refresh={fetchUsers}
          />
        )}

        {currentView === 'kahoot-details' && selectedKahoot && (
          <KahootDetailsView 
            kahoot={selectedKahoot} 
            onBack={() => {
              setSelectedKahoot(null);
              setCurrentView('dashboard');
            }}
          />
        )}
      </main>
    </div>
  );
}

// --- Sub-Views ---

const DashboardView = ({ kahoots, loading, onDelete, onSelect }) => (
  <div className="space-y-6">
    <div className="flex justify-between items-end">
      <div>
        <h1 className="text-3xl font-black text-slate-800 mb-2">My Kahoots</h1>
        <p className="text-slate-500">Manage your quizzes and games.</p>
      </div>
      <div className="text-sm font-bold text-slate-400">
        {kahoots.length} Kahoots
      </div>
    </div>

    {loading ? (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      </div>
    ) : kahoots.length === 0 ? (
      <div className="text-center py-20 bg-white rounded-xl border border-dashed border-slate-300">
        <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4 text-slate-400">
          <HelpCircle size={32} />
        </div>
        <h3 className="text-lg font-bold text-slate-700">No Kahoots yet</h3>
        <p className="text-slate-500 mb-6">Create your first quiz to get started!</p>
      </div>
    ) : (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {kahoots.map(kahoot => (
          <div 
            key={kahoot.id} 
            onClick={() => onSelect(kahoot)}
            className="group relative bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden hover:shadow-lg hover:-translate-y-1 transition-all cursor-pointer"
          >
            <div className="h-32 bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
               <FileText className="text-white opacity-20" size={48} />
            </div>
            <div className="p-5">
              <div className="flex justify-between items-start mb-2">
                <Badge color={kahoot.is_private ? 'purple' : 'green'}>
                  {kahoot.is_private ? 'Private' : 'Public'}
                </Badge>
              </div>
              <h3 className="font-bold text-lg text-slate-800 mb-1 group-hover:text-indigo-600 transition-colors">
                {kahoot.title}
              </h3>
              <p className="text-sm text-slate-500 line-clamp-2 h-10">
                {kahoot.description || "No description provided."}
              </p>
              
              <div className="mt-4 flex items-center justify-between pt-4 border-t border-slate-100">
                 <span className="text-xs font-bold text-slate-400">ID: {kahoot.id}</span>
                 <button 
                  onClick={(e) => onDelete(kahoot.id, e)}
                  className="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-full transition-colors"
                 >
                   <Trash2 size={16} />
                 </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    )}
  </div>
);

const CreateKahootView = ({ onSuccess, onCancel }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    language_id: 1, // Defaulting to 1 as we don't have a language picker in this basic demo
    is_private: false
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}/your_kahoot`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        alert("Kahoot created successfully!");
        onSuccess();
      } else {
        const err = await response.json();
        alert(`Error: ${err.detail}`);
      }
    } catch (error) {
      alert("Failed to connect to server");
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-6">
        <button onClick={onCancel} className="text-sm font-bold text-slate-500 hover:text-slate-800 mb-2">
          &larr; Back to Dashboard
        </button>
        <h1 className="text-3xl font-black text-slate-800">Create New Kahoot</h1>
      </div>

      <Card className="p-8">
        <form onSubmit={handleSubmit}>
          <Input 
            label="Title" 
            placeholder="e.g. History Trivia 101" 
            value={formData.title}
            onChange={e => setFormData({...formData, title: e.target.value})}
            required
          />
          
          <div className="mb-4">
            <label className="block text-sm font-semibold text-slate-700 mb-1">Description</label>
            <textarea
              className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
              rows="4"
              placeholder="What is this quiz about?"
              value={formData.description}
              onChange={e => setFormData({...formData, description: e.target.value})}
            ></textarea>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-6">
             <Select 
               label="Visibility"
               value={formData.is_private}
               onChange={e => setFormData({...formData, is_private: e.target.value === 'true'})}
               options={[
                 { label: 'Public', value: false },
                 { label: 'Private', value: true }
               ]}
             />
             <Input 
               label="Language ID"
               type="number"
               value={formData.language_id}
               onChange={e => setFormData({...formData, language_id: parseInt(e.target.value)})}
             />
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
            <Button variant="secondary" onClick={onCancel}>Cancel</Button>
            <Button type="submit" variant="primary">Create Kahoot</Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

const UsersView = ({ users, loading, onDelete, refresh }) => {
  const [showAddModal, setShowAddModal] = useState(false);
  const [newUser, setNewUser] = useState({
    username: '',
    email: '',
    password: '',
    birthdate: '',
    name: '',
    organisation: '',
    subscriptions_id: 1,
    language_id: 1,
    customer_type_id: 1
  });

  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}/user`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newUser)
      });
      
      if (response.ok) {
        setShowAddModal(false);
        setNewUser({ username: '', email: '', password: '', birthdate: '', name: '', organisation: '', subscriptions_id: 1, language_id: 1, customer_type_id: 1});
        refresh();
      } else {
        const data = await response.json();
        alert(`Error: ${data.detail}`);
      }
    } catch (err) {
      alert("Connection error");
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
           <h1 className="text-3xl font-black text-slate-800">Users</h1>
           <p className="text-slate-500">Manage registered users.</p>
        </div>
        <Button onClick={() => setShowAddModal(true)} variant="primary">
          <Plus size={18} /> Add User
        </Button>
      </div>

      {showAddModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-lg p-6 animate-in fade-in zoom-in duration-200">
            <h2 className="text-xl font-bold mb-4">Register New User</h2>
            <form onSubmit={handleCreateUser} className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <Input label="Username" value={newUser.username} onChange={e => setNewUser({...newUser, username: e.target.value})} required />
                <Input label="Name" value={newUser.name} onChange={e => setNewUser({...newUser, name: e.target.value})} />
              </div>
              <Input label="Email" type="email" value={newUser.email} onChange={e => setNewUser({...newUser, email: e.target.value})} required />
              <div className="grid grid-cols-2 gap-3">
                 <Input label="Password" type="password" value={newUser.password} onChange={e => setNewUser({...newUser, password: e.target.value})} required />
                 <Input label="Birthdate" type="date" value={newUser.birthdate} onChange={e => setNewUser({...newUser, birthdate: e.target.value})} required />
              </div>
              <Input label="Organisation" value={newUser.organisation} onChange={e => setNewUser({...newUser, organisation: e.target.value})} />
              
              <div className="flex justify-end gap-2 mt-4">
                <Button variant="secondary" onClick={() => setShowAddModal(false)}>Cancel</Button>
                <Button type="submit" variant="primary">Save User</Button>
              </div>
            </form>
          </Card>
        </div>
      )}

      <Card className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-xs uppercase text-slate-500 font-bold">
              <th className="p-4">ID</th>
              <th className="p-4">Username</th>
              <th className="p-4">Email</th>
              <th className="p-4">Name</th>
              <th className="p-4">Org</th>
              <th className="p-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-sm">
            {users.map(user => (
              <tr key={user.id} className="hover:bg-slate-50">
                <td className="p-4 font-mono text-slate-400">#{user.id}</td>
                <td className="p-4 font-bold text-slate-700">{user.username}</td>
                <td className="p-4 text-slate-600">{user.email}</td>
                <td className="p-4 text-slate-600">{user.name || '-'}</td>
                <td className="p-4 text-slate-600">{user.organisation || '-'}</td>
                <td className="p-4 text-right">
                  <button 
                    onClick={() => onDelete(user.username)}
                    className="text-slate-400 hover:text-red-600 transition-colors p-1"
                  >
                    <Trash2 size={16} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {users.length === 0 && !loading && (
          <div className="p-8 text-center text-slate-500">No users found.</div>
        )}
      </Card>
    </div>
  );
};

const KahootDetailsView = ({ kahoot, onBack }) => {
  const [questionType, setQuestionType] = useState('true_false'); // true_false or written
  const [tfQuestion, setTfQuestion] = useState({ question: '', answer: true });
  const [writtenQuestion, setWrittenQuestion] = useState({ question: '' });
  
  // NOTE: The backend doesn't support fetching questions for a specific Kahoot in the provided 'app.py' snippet.
  // We can only Add questions blindly.
  const [addedQuestionsLog, setAddedQuestionsLog] = useState([]);

  const addTrueFalse = async (e) => {
    e.preventDefault();
    const payload = { ...tfQuestion, your_kahoot_id: kahoot.id };
    
    try {
      const res = await fetch(`${API_BASE_URL}/true_false_quiz`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        setAddedQuestionsLog(prev => [{...payload, type: 'TF', id: Date.now()}, ...prev]);
        setTfQuestion({ question: '', answer: true });
        alert("True/False Question Added!");
      } else {
        alert("Failed to add question");
      }
    } catch (err) { alert("Error connecting"); }
  };

  const addWritten = async (e) => {
    e.preventDefault();
    const payload = { ...writtenQuestion, your_kahoot_id: kahoot.id };
    
    try {
      const res = await fetch(`${API_BASE_URL}/written_quiz`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        setAddedQuestionsLog(prev => [{...payload, type: 'Written', id: Date.now()}, ...prev]);
        setWrittenQuestion({ question: '' });
        alert("Written Question Added!");
      } else {
        alert("Failed to add question");
      }
    } catch (err) { alert("Error connecting"); }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <button onClick={onBack} className="p-2 hover:bg-slate-200 rounded-full text-slate-500">
           &larr; Back
        </button>
        <div>
           <h1 className="text-3xl font-black text-slate-800">{kahoot.title}</h1>
           <p className="text-slate-500">{kahoot.description}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Editor Column */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="p-6">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <Plus size={20} className="text-indigo-600"/> Add Question
            </h2>
            
            <div className="flex gap-2 mb-6 p-1 bg-slate-100 rounded-lg w-fit">
              <button 
                onClick={() => setQuestionType('true_false')}
                className={`px-4 py-2 rounded-md text-sm font-bold transition-all ${questionType === 'true_false' ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500'}`}
              >
                True / False
              </button>
              <button 
                onClick={() => setQuestionType('written')}
                className={`px-4 py-2 rounded-md text-sm font-bold transition-all ${questionType === 'written' ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500'}`}
              >
                Written Answer
              </button>
            </div>

            {questionType === 'true_false' ? (
              <form onSubmit={addTrueFalse} className="space-y-4">
                <Input 
                  label="Question Text" 
                  value={tfQuestion.question} 
                  onChange={e => setTfQuestion({...tfQuestion, question: e.target.value})} 
                  placeholder="e.g. The sky is blue."
                  required 
                />
                <div>
                   <label className="block text-sm font-semibold text-slate-700 mb-2">Correct Answer</label>
                   <div className="flex gap-4">
                     <button
                       type="button"
                       onClick={() => setTfQuestion({...tfQuestion, answer: true})}
                       className={`flex-1 py-4 rounded-lg font-black text-white transition-transform active:scale-95 ${tfQuestion.answer ? 'bg-blue-600 ring-4 ring-blue-200' : 'bg-slate-300'}`}
                     >
                       TRUE
                     </button>
                     <button
                       type="button"
                       onClick={() => setTfQuestion({...tfQuestion, answer: false})}
                       className={`flex-1 py-4 rounded-lg font-black text-white transition-transform active:scale-95 ${!tfQuestion.answer ? 'bg-red-500 ring-4 ring-red-200' : 'bg-slate-300'}`}
                     >
                       FALSE
                     </button>
                   </div>
                </div>
                <div className="pt-4 text-right">
                  <Button type="submit" variant="primary">Add to Kahoot</Button>
                </div>
              </form>
            ) : (
              <form onSubmit={addWritten} className="space-y-4">
                <Input 
                  label="Question Text" 
                  value={writtenQuestion.question} 
                  onChange={e => setWrittenQuestion({...writtenQuestion, question: e.target.value})} 
                  placeholder="e.g. What is the capital of France?"
                  required 
                />
                <div className="bg-yellow-50 p-4 rounded-lg text-sm text-yellow-800 border border-yellow-200">
                  <p><strong>Note:</strong> After adding a written question, you must add valid answers separately using the <code>/quiz_answer</code> endpoint in a more advanced view. This form only creates the question stem.</p>
                </div>
                <div className="pt-4 text-right">
                  <Button type="submit" variant="primary">Create Question Stem</Button>
                </div>
              </form>
            )}
          </Card>
        </div>

        {/* Local History Column */}
        <div>
           <Card className="p-6 h-full">
             <h3 className="font-bold text-slate-700 mb-4 flex items-center gap-2">
               <Settings size={18} /> Session Log
             </h3>
             <p className="text-xs text-slate-500 mb-4">
               Questions added in this session. (The API does not support fetching existing questions yet).
             </p>

             <div className="space-y-3">
               {addedQuestionsLog.length === 0 && (
                 <p className="text-sm italic text-slate-400">No questions added yet.</p>
               )}
               {addedQuestionsLog.map((q) => (
                 <div key={q.id} className="p-3 bg-slate-50 rounded-lg border border-slate-100 text-sm">
                   <div className="flex justify-between mb-1">
                      <span className="font-bold text-slate-700">{q.type === 'TF' ? 'True/False' : 'Written'}</span>
                      {q.type === 'TF' && (
                        <span className={`text-xs font-bold px-2 py-0.5 rounded ${q.answer ? 'bg-blue-100 text-blue-700' : 'bg-red-100 text-red-700'}`}>
                          {q.answer ? 'True' : 'False'}
                        </span>
                      )}
                   </div>
                   <p className="text-slate-600">{q.question}</p>
                 </div>
               ))}
             </div>
           </Card>
        </div>
      </div>
    </div>
  );
};