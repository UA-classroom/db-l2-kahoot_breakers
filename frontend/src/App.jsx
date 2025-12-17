import React, { useState, useEffect } from 'react';
import { 
  Layout, 
  Plus, 
  Trash2, 
  Users, 
  MessageSquare, 
  Check, 
  Edit2, 
  Tv, 
  X,
  Settings,
  AlertCircle
} from 'lucide-react';

// Connects directly to your Uvicorn backend
const API_BASE_URL = 'http://127.0.0.1:8000';

// --- UI COMPONENTS ---

const Button = ({ children, onClick, variant = 'primary', className = "", type = "button" }) => {
  const baseStyle = "px-4 py-2 rounded-lg font-bold transition-all flex items-center justify-center gap-2 text-sm shadow-sm active:scale-95";
  const variants = {
    primary: "bg-indigo-600 text-white hover:bg-indigo-700",
    secondary: "bg-white border border-slate-300 text-slate-700 hover:bg-slate-50",
    danger: "bg-red-50 text-red-600 border border-red-200 hover:bg-red-100",
    ghost: "text-slate-500 hover:text-slate-800 hover:bg-slate-100"
  };
  return (
    <button type={type} onClick={onClick} className={`${baseStyle} ${variants[variant]} ${className}`}>
      {children}
    </button>
  );
};

const Input = ({ label, type = "text", value, onChange, placeholder, required = false }) => (
  <div className="mb-3">
    {label && <label className="block text-xs font-bold text-slate-500 uppercase mb-1">{label}</label>}
    <input
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      required={required}
      className="w-full px-3 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-sm"
    />
  </div>
);

const Select = ({ label, value, onChange, options }) => (
  <div className="mb-3">
    {label && <label className="block text-xs font-bold text-slate-500 uppercase mb-1">{label}</label>}
    <select
      value={value}
      onChange={onChange}
      className="w-full px-3 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-indigo-500 outline-none transition-all bg-white text-sm"
    >
      {options.map((opt) => (
        <option key={opt.value} value={opt.value}>{opt.label}</option>
      ))}
    </select>
  </div>
);

const TabButton = ({ label, active, onClick, icon }) => (
  <button 
    onClick={onClick}
    className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-bold transition-all ${active ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
  >
    {icon} {label}
  </button>
);

// --- MAIN APP COMPONENT ---

export default function App() {
  const [view, setView] = useState('kahoots'); // 'kahoots', 'users', 'groups', 'kahoot-detail'
  const [selectedKahoot, setSelectedKahoot] = useState(null);

  return (
    <div className="flex min-h-screen bg-slate-50 font-sans text-slate-900">
      
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 fixed h-full z-10 hidden md:flex flex-col">
        <div className="p-6 border-b border-slate-100 flex items-center gap-3">
          <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-bold shadow-sm">K!</div>
          <span className="font-extrabold text-xl tracking-tight text-slate-800">KahootDB</span>
        </div>
        <nav className="p-4 space-y-1 flex-1">
          <NavItem 
            icon={<Layout size={20}/>} 
            label="My Kahoots" 
            active={view === 'kahoots' || view === 'kahoot-detail'} 
            onClick={() => setView('kahoots')} 
          />
          <NavItem 
            icon={<Users size={20}/>} 
            label="Users" 
            active={view === 'users'} 
            onClick={() => setView('users')} 
          />
          <NavItem 
            icon={<MessageSquare size={20}/>} 
            label="Groups" 
            active={view === 'groups'} 
            onClick={() => setView('groups')} 
          />
        </nav>
        <div className="p-4 border-t border-slate-100">
           <div className="bg-slate-50 p-3 rounded-lg border border-slate-100 text-xs text-slate-500">
              <p className="font-bold text-slate-700">Admin Mode</p>
              <p>Connected to Local DB</p>
           </div>
        </div>
      </aside>

      {/* Content Area */}
      <main className="flex-1 md:ml-64 p-8">
        {view === 'kahoots' && (
          <KahootsView onSelect={(k) => { setSelectedKahoot(k); setView('kahoot-detail'); }} />
        )}
        {view === 'users' && <UsersView />}
        {view === 'groups' && <GroupsView />}
        {view === 'kahoot-detail' && selectedKahoot && (
          <KahootDetailView 
            kahoot={selectedKahoot} 
            onBack={() => { setSelectedKahoot(null); setView('kahoots'); }} 
          />
        )}
      </main>
    </div>
  );
}

const NavItem = ({ icon, label, active, onClick }) => (
  <button 
    onClick={onClick}
    className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-bold transition-colors ${active ? 'bg-indigo-50 text-indigo-700' : 'text-slate-600 hover:bg-slate-50'}`}
  >
    {icon} {label}
  </button>
);

// --- 1. KAHOOTS VIEW ---
const KahootsView = ({ onSelect }) => {
  const [kahoots, setKahoots] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [newKahoot, setNewKahoot] = useState({ title: '', description: '', is_private: false, language_id: 1 });

  const fetchKahoots = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/your_kahoots`);
      if (res.ok) setKahoots(await res.json());
    } catch (e) { console.error("API Error:", e); }
  };

  useEffect(() => { fetchKahoots(); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_BASE_URL}/your_kahoots`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newKahoot)
      });
      if (res.ok) {
        setShowForm(false);
        setNewKahoot({ title: '', description: '', is_private: false, language_id: 1 });
        fetchKahoots();
      } else {
        const err = await res.json();
        alert(`Failed: ${err.detail || "Check if Language ID exists in DB"}`);
      }
    } catch(err) { alert("Connection Error"); }
  };

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if(!window.confirm("Delete this kahoot?")) return;
    const res = await fetch(`${API_BASE_URL}/your_kahoots/${id}`, { method: 'DELETE' });
    if (res.ok) fetchKahoots();
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-black text-slate-800">Your Kahoots</h1>
          <p className="text-slate-500">Manage games and quizzes.</p>
        </div>
        <Button onClick={() => setShowForm(!showForm)} variant="primary"><Plus size={18}/> New Kahoot</Button>
      </div>

      {showForm && (
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm mb-6 animate-in fade-in slide-in-from-top-4">
          <h3 className="font-bold text-lg mb-4 text-slate-700">Create New Kahoot</h3>
          <form onSubmit={handleCreate}>
            <div className="grid grid-cols-2 gap-4">
              <Input label="Title" value={newKahoot.title} onChange={e => setNewKahoot({...newKahoot, title: e.target.value})} required />
              <Input label="Description" value={newKahoot.description} onChange={e => setNewKahoot({...newKahoot, description: e.target.value})} />
            </div>
            <div className="grid grid-cols-2 gap-4">
               <Select label="Visibility" value={newKahoot.is_private} onChange={e => setNewKahoot({...newKahoot, is_private: e.target.value === 'true'})} 
                 options={[{label: 'Public', value: false}, {label: 'Private', value: true}]} />
               <Input type="number" label="Language ID" value={newKahoot.language_id} onChange={e => setNewKahoot({...newKahoot, language_id: parseInt(e.target.value)})} required />
            </div>
            <div className="flex justify-end gap-2 mt-4">
              <Button variant="secondary" onClick={() => setShowForm(false)}>Cancel</Button>
              <Button type="submit" variant="primary">Save Kahoot</Button>
            </div>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {kahoots.map(k => (
          <div key={k.id} onClick={() => onSelect(k)} className="group bg-white rounded-xl border border-slate-200 p-5 cursor-pointer hover:shadow-md hover:border-indigo-300 transition-all">
            <div className="flex justify-between items-start mb-2">
              <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded ${k.is_private ? 'bg-purple-100 text-purple-700' : 'bg-green-100 text-green-700'}`}>
                {k.is_private ? 'Private' : 'Public'}
              </span>
              <button onClick={(e) => handleDelete(k.id, e)} className="text-slate-400 hover:text-red-600 p-1 rounded-full hover:bg-red-50"><Trash2 size={16}/></button>
            </div>
            <h3 className="font-bold text-lg text-slate-800 mb-1 group-hover:text-indigo-600">{k.title}</h3>
            <p className="text-sm text-slate-500 line-clamp-2">{k.description || "No description."}</p>
          </div>
        ))}
        {kahoots.length === 0 && !showForm && (
            <div className="col-span-full py-10 text-center text-slate-400 border-2 border-dashed border-slate-200 rounded-xl">
                No Kahoots found. Create one above!
            </div>
        )}
      </div>
    </div>
  );
};

// --- 2. USERS VIEW ---
const UsersView = () => {
  const [users, setUsers] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [newUser, setNewUser] = useState({
    username: '', email: '', password: '', birthdate: '', name: '', organisation: '',
    subscriptions_id: 1, language_id: 1, customer_type_id: 1
  });

  const fetchUsers = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/users`);
      if (res.ok) setUsers(await res.json());
    } catch(e) { console.error(e); }
  };

  useEffect(() => { fetchUsers(); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_BASE_URL}/users`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(newUser)
      });
      if (res.ok) {
        setShowForm(false);
        fetchUsers();
        setNewUser({ username: '', email: '', password: '', birthdate: '', name: '', organisation: '', subscriptions_id: 1, language_id: 1, customer_type_id: 1 });
      } else {
        const err = await res.json();
        alert(`Error: ${err.detail}`);
      }
    } catch(err) { alert("Connection Error"); }
  };

  const handleDelete = async (username) => {
    if(!window.confirm(`Delete user ${username}?`)) return;
    const res = await fetch(`${API_BASE_URL}/users/${username}`, { method: 'DELETE' });
    if(res.ok) fetchUsers();
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-black text-slate-800">Users Directory</h1>
        <Button onClick={() => setShowForm(!showForm)} variant="primary"><Plus size={18}/> Add User</Button>
      </div>

      {showForm && (
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm animate-in fade-in slide-in-from-top-4">
          <form onSubmit={handleCreate} className="grid grid-cols-2 gap-4">
             <Input label="Username" value={newUser.username} onChange={e => setNewUser({...newUser, username: e.target.value})} required />
             <Input label="Email" type="email" value={newUser.email} onChange={e => setNewUser({...newUser, email: e.target.value})} required />
             <Input label="Password" type="password" value={newUser.password} onChange={e => setNewUser({...newUser, password: e.target.value})} required />
             <Input label="Birthdate" type="date" value={newUser.birthdate} onChange={e => setNewUser({...newUser, birthdate: e.target.value})} required />
             <Input label="Name" value={newUser.name} onChange={e => setNewUser({...newUser, name: e.target.value})} />
             <Input label="Organisation" value={newUser.organisation} onChange={e => setNewUser({...newUser, organisation: e.target.value})} />
             
             <div className="col-span-2 flex gap-4 bg-slate-50 p-3 rounded-lg border border-slate-200">
                <Input label="Sub ID" type="number" value={newUser.subscriptions_id} onChange={e => setNewUser({...newUser, subscriptions_id: parseInt(e.target.value)})} required />
                <Input label="Lang ID" type="number" value={newUser.language_id} onChange={e => setNewUser({...newUser, language_id: parseInt(e.target.value)})} required />
                <Input label="Type ID" type="number" value={newUser.customer_type_id} onChange={e => setNewUser({...newUser, customer_type_id: parseInt(e.target.value)})} required />
             </div>
             <div className="col-span-2 flex justify-end gap-2">
                <Button variant="secondary" onClick={() => setShowForm(false)}>Cancel</Button>
                <Button type="submit" variant="primary">Create User</Button>
             </div>
          </form>
        </div>
      )}

      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-200 bg-slate-50 text-xs font-bold text-slate-500 uppercase">
              <th className="p-4">ID</th>
              <th className="p-4">Username</th>
              <th className="p-4">Email</th>
              <th className="p-4">Name</th>
              <th className="p-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="text-sm divide-y divide-slate-100">
            {users.map(u => (
              <tr key={u.id} className="hover:bg-slate-50">
                <td className="p-4 text-slate-400 font-mono">#{u.id}</td>
                <td className="p-4 font-bold text-slate-700">{u.username}</td>
                <td className="p-4">{u.email}</td>
                <td className="p-4">{u.name || '-'}</td>
                <td className="p-4 text-right">
                  <button onClick={() => handleDelete(u.username)} className="text-slate-400 hover:text-red-600"><Trash2 size={16}/></button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// --- 3. GROUPS VIEW ---
const GroupsView = () => {
  const [groups, setGroups] = useState([]);
  const [newGroup, setNewGroup] = useState({ name: '', description: '' });

  const fetchGroups = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/groups`);
      if (res.ok) setGroups(await res.json());
    } catch(e) {}
  };

  useEffect(() => { fetchGroups(); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    const res = await fetch(`${API_BASE_URL}/groups`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(newGroup)
    });
    if (res.ok) {
      setNewGroup({ name: '', description: '' });
      fetchGroups();
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this group?")) return;
    try {
        const res = await fetch(`${API_BASE_URL}/groups/${id}`, { method: 'DELETE' });
        if (res.ok) {
            fetchGroups();
        } else {
            const err = await res.json();
            // Shows database error if tables are stuck on RESTRICT
            alert(`Failed to delete: ${err.detail}`); 
        }
    } catch (e) {
        alert("Error connecting to server");
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="md:col-span-2 space-y-6">
        <h1 className="text-2xl font-black text-slate-800">Groups</h1>
        <div className="grid grid-cols-1 gap-4">
          {groups.map(g => (
            <div key={g.id} className="bg-white rounded-xl border border-slate-200 p-4 flex justify-between items-center shadow-sm hover:shadow-md transition-all">
              <div>
                <h3 className="font-bold text-lg text-slate-700">{g.name}</h3>
                <p className="text-slate-500 text-sm">{g.description}</p>
                <span className="inline-block mt-2 bg-slate-100 text-slate-400 text-[10px] px-2 py-0.5 rounded font-mono">ID: {g.id}</span>
              </div>
              <button 
                onClick={() => handleDelete(g.id)} 
                className="p-2 text-slate-300 hover:text-red-500 hover:bg-red-50 rounded-full transition-colors"
                title="Delete Group"
              >
                <Trash2 size={18} />
              </button>
            </div>
          ))}
          {groups.length === 0 && <p className="text-slate-400 italic">No groups found.</p>}
        </div>
      </div>
      <div>
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm sticky top-6">
          <h2 className="font-bold mb-4 text-slate-700">Create Group</h2>
          <form onSubmit={handleCreate} className="space-y-4">
            <Input label="Name" value={newGroup.name} onChange={e => setNewGroup({...newGroup, name: e.target.value})} required />
            <Input label="Description" value={newGroup.description} onChange={e => setNewGroup({...newGroup, description: e.target.value})} />
            <Button type="submit" variant="primary" className="w-full">Save Group</Button>
          </form>
        </div>
      </div>
    </div>
  );
};

// --- 4. KAHOOT DETAIL VIEW ---
const KahootDetailView = ({ kahoot, onBack }) => {
  const [activeTab, setActiveTab] = useState('tf'); 
  const [tfData, setTfData] = useState({ question: '', answer: true });
  const [writtenData, setWrittenData] = useState({ question: '' });
  const [classicData, setClassicData] = useState({ title: '', text: '' });
  
  // List to hold both DB questions + newly added ones
  const [questionList, setQuestionList] = useState([]);

  // Fetch Questions from DB on Load
  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/your_kahoots/${kahoot.id}/questions`);
        if (res.ok) {
          const data = await res.json();
          setQuestionList(data);
        }
      } catch (e) {
        console.error("Failed to load questions", e);
      }
    };
    fetchQuestions();
  }, [kahoot.id]);

  // Helper to add to list locally for instant feedback
  const addLocalItem = (type, content, extra = {}) => {
    const newItem = { 
      id: `temp-${Date.now()}`, 
      type: type, 
      question: content,
      ...extra 
    };
    setQuestionList(prev => [newItem, ...prev]);
  };

  const handleAddTF = async (e) => {
    e.preventDefault();
    const payload = { ...tfData, your_kahoot_id: kahoot.id };
    try {
      const res = await fetch(`${API_BASE_URL}/quizzes/true_false`, {
        method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)
      });
      if(res.ok) {
        addLocalItem('True/False', tfData.question, { answer: tfData.answer });
        setTfData({ question: '', answer: true });
      } else { alert("Failed to add question"); }
    } catch(err) { alert("Error connecting"); }
  };

  const handleAddWritten = async (e) => {
    e.preventDefault();
    const payload = { ...writtenData, your_kahoot_id: kahoot.id };
    try {
      const res = await fetch(`${API_BASE_URL}/quizzes/written_question`, {
        method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)
      });
      if(res.ok) {
        addLocalItem('Written', writtenData.question);
        setWrittenData({ question: '' });
        alert("Question stem created. (Add answers via API directly)");
      } else { alert("Failed to add question"); }
    } catch(err) { alert("Error connecting"); }
  };

  const handleAddClassic = async (e) => {
    e.preventDefault();
    const payload = { ...classicData, your_kahoot_id: kahoot.id };
    try {
      const res = await fetch(`${API_BASE_URL}/classic_presentations`, {
        method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)
      });
      if(res.ok) {
        addLocalItem('Slide', classicData.title);
        setClassicData({ title: '', text: '' });
      } else { alert("Failed to add slide"); }
    } catch(err) { alert("Error connecting"); }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="flex items-center gap-4 mb-8">
        <button onClick={onBack} className="p-2 hover:bg-slate-200 rounded-full text-slate-500 transition-colors"><X size={20}/></button>
        <div>
          <h1 className="text-3xl font-black text-slate-800">{kahoot.title}</h1>
          <p className="text-slate-500">{kahoot.description}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        
        {/* Editor Area */}
        <div className="md:col-span-2 space-y-4">
          <div className="flex gap-2 bg-slate-200 p-1 rounded-lg w-fit">
            <TabButton label="True/False" active={activeTab === 'tf'} onClick={() => setActiveTab('tf')} icon={<Check size={16}/>} />
            <TabButton label="Written" active={activeTab === 'written'} onClick={() => setActiveTab('written')} icon={<Edit2 size={16}/>} />
            <TabButton label="Presentation" active={activeTab === 'classic'} onClick={() => setActiveTab('classic')} icon={<Tv size={16}/>} />
          </div>

          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm transition-all">
            {activeTab === 'tf' && (
              <form onSubmit={handleAddTF} className="space-y-4 animate-in fade-in slide-in-from-left-2">
                <h3 className="font-bold text-slate-700 border-b pb-2">Add True/False Question</h3>
                <Input label="Question" value={tfData.question} onChange={e => setTfData({...tfData, question: e.target.value})} required />
                <div>
                   <label className="block text-xs font-bold text-slate-500 uppercase mb-2">Correct Answer</label>
                   <div className="flex gap-4">
                     <button type="button" onClick={() => setTfData({...tfData, answer: true})} className={`flex-1 py-3 rounded font-bold transition-all ${tfData.answer ? 'bg-blue-600 text-white shadow-md' : 'bg-slate-100 text-slate-500'}`}>TRUE</button>
                     <button type="button" onClick={() => setTfData({...tfData, answer: false})} className={`flex-1 py-3 rounded font-bold transition-all ${!tfData.answer ? 'bg-red-500 text-white shadow-md' : 'bg-slate-100 text-slate-500'}`}>FALSE</button>
                   </div>
                </div>
                <Button type="submit" variant="primary" className="w-full mt-4">Add to Kahoot</Button>
              </form>
            )}

            {activeTab === 'written' && (
              <form onSubmit={handleAddWritten} className="space-y-4 animate-in fade-in slide-in-from-left-2">
                <h3 className="font-bold text-slate-700 border-b pb-2">Add Written Question</h3>
                <Input label="Question Text" value={writtenData.question} onChange={e => setWrittenData({...writtenData, question: e.target.value})} required />
                <div className="flex items-start gap-2 bg-yellow-50 text-yellow-800 p-4 rounded text-sm border border-yellow-200">
                   <AlertCircle size={16} className="mt-0.5"/>
                   <p>Note: This creates the question stem only. You must create valid answers separately using the <code>/quizzes/written_answers</code> endpoint.</p>
                </div>
                <Button type="submit" variant="primary" className="w-full">Create Question</Button>
              </form>
            )}

            {activeTab === 'classic' && (
               <form onSubmit={handleAddClassic} className="space-y-4 animate-in fade-in slide-in-from-left-2">
                 <h3 className="font-bold text-slate-700 border-b pb-2">Add Presentation Slide</h3>
                 <Input label="Slide Title" value={classicData.title} onChange={e => setClassicData({...classicData, title: e.target.value})} required />
                 <div>
                   <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Content Text</label>
                   <textarea className="w-full border border-slate-300 rounded-lg p-3 text-sm focus:ring-2 focus:ring-indigo-500 outline-none" rows="4" placeholder="Content..." value={classicData.text} onChange={e => setClassicData({...classicData, text: e.target.value})}></textarea>
                 </div>
                 <Button type="submit" variant="primary" className="w-full">Add Slide</Button>
               </form>
            )}
          </div>
        </div>

        {/* --- QUESTIONS LIST --- */}
        <div>
          <div className="p-4 h-full bg-slate-50 border border-slate-200 rounded-xl flex flex-col">
            <h3 className="font-bold text-slate-500 uppercase text-xs mb-4 flex items-center gap-2">
              <Settings size={14}/> Questions ({questionList.length})
            </h3>
            
            <div className="space-y-3 flex-1 overflow-y-auto max-h-[600px] pr-2 custom-scrollbar">
              {questionList.length === 0 && <p className="text-slate-400 text-sm italic text-center mt-10">No questions yet.</p>}
              
              {questionList.map((item, idx) => (
                <div key={item.id || idx} className="bg-white p-3 rounded-lg border border-slate-200 shadow-sm text-sm hover:border-indigo-300 transition-colors">
                  <div className="flex justify-between items-center text-xs text-slate-400 mb-1">
                    <span className="font-bold text-indigo-600 uppercase">{item.type}</span>
                    
                    {/* Visual Badge for True/False */}
                    {(item.type === 'True/False' || item.type === 'TF') && (
                       <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${item.answer ? 'bg-blue-100 text-blue-700' : 'bg-red-100 text-red-700'}`}>
                         {item.answer ? 'TRUE' : 'FALSE'}
                       </span>
                    )}
                  </div>
                  <p className="font-semibold text-slate-700 leading-snug">{item.question}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};