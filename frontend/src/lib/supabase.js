import { createClient } from '@supabase/supabase-js';

// Initialize Supabase client
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error('Missing Supabase environment variables');
}

export const supabase = createClient(
  supabaseUrl || '',
  supabaseKey || ''
);

// Authentication helpers
export async function signIn({ email, password }) {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });
  
  return { data, error };
}

export async function signUp({ email, password }) {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
  });
  
  return { data, error };
}

export async function signOut() {
  const { error } = await supabase.auth.signOut();
  return { error };
}

export async function getCurrentUser() {
  const { data, error } = await supabase.auth.getUser();
  return { user: data?.user, error };
}

export async function getSession() {
  const { data, error } = await supabase.auth.getSession();
  return { session: data?.session, error };
}

// History helpers
export async function saveHistory(userId, urls, resultCount) {
  const { data, error } = await supabase
    .from('scrape_history')
    .insert([
      { 
        user_id: userId,
        urls: urls,
        image_count: resultCount,
        created_at: new Date()
      }
    ]);
  
  return { data, error };
}

export async function getUserHistory(userId) {
  const { data, error } = await supabase
    .from('scrape_history')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false });
  
  return { data, error };
}
