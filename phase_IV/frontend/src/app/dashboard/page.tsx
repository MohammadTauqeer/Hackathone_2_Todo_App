'use client';

import { useState, useEffect, useMemo } from 'react';
import ProtectedRoute from '@/components/protected-route';
import Header from '@/components/header';
import { Card, CardContent } from '@/components/ui/card';
import { useAuth } from '@/context/auth-context';
import { 
  Plus, Sparkles, Trash2, Edit2, CheckCircle, Circle, 
  Activity, Search, Wand2 
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { taskService, chatService } from '@/lib/api';

export default function DashboardPage() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<any[]>([]);
  const [newTask, setNewTask] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [filter, setFilter] = useState('all');
  const [aiCommand, setAiCommand] = useState('');
  const [isAiLoading, setIsAiLoading] = useState(false);
  
  // Hydration protection
  const [mounted, setMounted] = useState(false);
  useEffect(() => { setMounted(true); }, []);

  useEffect(() => {
    if (mounted && user) { loadTasks(); }
  }, [mounted, user]);

  const loadTasks = async () => {
    try {
      const response = await taskService.fetchTasks();
      setTasks(Array.isArray(response.tasks) ? response.tasks : []);
    } catch (error) { console.error("Load error:", error); }
  };

  const filteredTasks = useMemo(() => {
    if (!tasks) return [];
    return tasks.filter(task => {
      const matchesSearch = task.title.toLowerCase().includes(searchQuery.toLowerCase());
      if (filter === 'active') return matchesSearch && !task.completed;
      if (filter === 'completed') return matchesSearch && task.completed;
      return matchesSearch;
    });
  }, [tasks, searchQuery, filter]);

  const handleAiExecute = async () => {
    if (!aiCommand.trim()) return;
    setIsAiLoading(true);
    try {
      await chatService.sendMessage(aiCommand);
      setAiCommand('');
      setTimeout(loadTasks, 1000); 
    } catch (error) { console.error("AI Error:", error); } 
    finally { setIsAiLoading(false); }
  };

  // Pre-render check to solve SSR issues
  if (!mounted) return null;

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-[#fcfaff]">
        <Header />
        <main className="container mx-auto p-8 max-w-5xl">
          <div className="flex justify-between items-start mb-10">
            <div>
              <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight">Dashboard</h1>
              <p className="text-slate-500 font-medium">Manage your tasks efficiently, {user?.username}.</p>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" className="bg-purple-50 text-purple-700 border-purple-100"><Sparkles className="mr-2 h-4 w-4" /> Magic Assistant</Button>
              <Button variant="outline" className="bg-purple-50 text-purple-700 border-purple-100"><Activity className="mr-2 h-4 w-4" /> AI Suggestions</Button>
            </div>
          </div>

          <Card className="mb-6 shadow-sm border-none rounded-2xl bg-white overflow-hidden">
            <CardContent className="p-6">
              <div className="flex items-center gap-2 mb-3 text-purple-600 font-bold"><Wand2 className="h-5 w-5" /><span>AI Task Assistant</span></div>
              <div className="flex gap-3">
                <Input value={aiCommand} onChange={(e) => setAiCommand(e.target.value)} placeholder="Type your command..." className="flex-1 h-12 bg-slate-50 border-none rounded-xl" />
                <Button onClick={handleAiExecute} disabled={isAiLoading} className="h-12 bg-purple-600 px-8 text-white font-bold rounded-xl">{isAiLoading ? "..." : "Execute"}</Button>
              </div>
            </CardContent>
          </Card>

          <Card className="mb-8 shadow-sm border-none rounded-2xl bg-white">
            <CardContent className="p-6">
              <div className="flex gap-3">
                <Input value={newTask} onChange={(e) => setNewTask(e.target.value)} placeholder="What needs to be done?" className="flex-1 h-12 bg-slate-50 border-none rounded-xl" />
                <Button onClick={async () => { if(!newTask.trim()) return; await taskService.addTask(newTask); setNewTask(''); loadTasks(); }} className="h-12 bg-purple-400 px-8 text-white font-bold rounded-xl"><Plus className="mr-2" /> Add</Button>
              </div>
            </CardContent>
          </Card>

          <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
            <div className="relative flex-1 min-w-[300px]">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 text-slate-400" />
              <Input placeholder="Search tasks..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="pl-10 h-12 bg-white border-slate-100 rounded-xl" />
            </div>
            <div className="flex gap-1 bg-white p-1 rounded-xl border border-slate-100">
              {['all', 'active', 'completed'].map((f) => (
                <Button key={f} variant={filter === f ? 'secondary' : 'ghost'} onClick={() => setFilter(f)} className="capitalize px-6 rounded-lg">{f}</Button>
              ))}
            </div>
          </div>

          <div className="space-y-4">
            {filteredTasks.map((task) => (
              <Card key={task.id} className="p-6 border-none shadow-sm bg-white border-l-4 border-l-purple-500 group">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <button onClick={async () => { await taskService.updateTask(task.id, { completed: !task.completed }); loadTasks(); }}>
                      {task.completed ? <CheckCircle className="text-green-500 h-6 w-6" /> : <Circle className="text-slate-200 h-6 w-6" />}
                    </button>
                    <span className={`font-bold text-lg ${task.completed ? 'line-through text-slate-300' : 'text-slate-700'}`}>{task.title}</span>
                  </div>
                  <div className="flex gap-2">
                    <Button variant="ghost" size="icon" onClick={async () => { await taskService.deleteTask(task.id); loadTasks(); }} className="text-slate-300 hover:text-red-500"><Trash2 className="h-5 w-5" /></Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
