import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { 
  LineChart, Line, AreaChart, Area, BarChart, Bar, 
  PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, 
  Tooltip, Legend, ResponsiveContainer 
} from 'recharts';

// Sample data - will be replaced with API data in production
const progressData = [
  { name: 'Week 1', completed: 5, target: 7 },
  { name: 'Week 2', completed: 8, target: 7 },
  { name: 'Week 3', completed: 6, target: 7 },
  { name: 'Week 4', completed: 9, target: 7 },
  { name: 'Week 5', completed: 11, target: 7 },
  { name: 'Week 6', completed: 8, target: 7 },
];

const skillsData = [
  { name: 'Programming', value: 75 },
  { name: 'Data Science', value: 60 },
  { name: 'Design', value: 45 },
  { name: 'Business', value: 30 },
  { name: 'Marketing', value: 20 },
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

const Dashboard = () => {
  const [learningData, setLearningData] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [topCourses, setTopCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch user learning data
    const fetchLearningData = async () => {
      try {
        const response = await fetch('/api/user/learning-progress');
        if (!response.ok) throw new Error('Failed to fetch learning data');
        const data = await response.json();
        setLearningData(data);
      } catch (err) {
        setError('Error loading learning data');
        console.error(err);
        // Use sample data as fallback
        setLearningData({
          progressData,
          skillsData,
          completedCourses: 12,
          totalHours: 48,
          streak: 7
        });
      }
    };

    // Fetch personalized recommendations
    const fetchRecommendations = async () => {
      try {
        const response = await fetch('/api/recommendations/personalized');
        if (!response.ok) throw new Error('Failed to fetch recommendations');
        const data = await response.json();
        setRecommendations(data);
      } catch (err) {
        setError('Error loading recommendations');
        console.error(err);
        // Sample fallback data
        setRecommendations([
          { id: 1, title: 'Machine Learning Fundamentals', category: 'Data Science', rating: 4.8, image: '/images/course1.jpg' },
          { id: 2, title: 'Advanced React Patterns', category: 'Programming', rating: 4.7, image: '/images/course2.jpg' },
          { id: 3, title: 'Data Visualization with D3', category: 'Data Science', rating: 4.5, image: '/images/course3.jpg' },
          { id: 4, title: 'UX Design Principles', category: 'Design', rating: 4.6, image: '/images/course4.jpg' },
        ]);
      }
    };

    // Fetch trending/popular courses
    const fetchTopCourses = async () => {
      try {
        const response = await fetch('/api/courses/trending');
        if (!response.ok) throw new Error('Failed to fetch top courses');
        const data = await response.json();
        setTopCourses(data);
      } catch (err) {
        setError('Error loading top courses');
        console.error(err);
        // Sample fallback data
        setTopCourses([
          { id: 5, title: 'Python for Beginners', category: 'Programming', rating: 4.9, image: '/images/course5.jpg' },
          { id: 6, title: 'Web Development Bootcamp', category: 'Programming', rating: 4.8, image: '/images/course6.jpg' },
          { id: 7, title: 'Digital Marketing Essentials', category: 'Marketing', rating: 4.6, image: '/images/course7.jpg' },
          { id: 8, title: 'Business Analytics', category: 'Business', rating: 4.7, image: '/images/course8.jpg' },
        ]);
      }
    };

    Promise.all([fetchLearningData(), fetchRecommendations(), fetchTopCourses()])
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>Learning Dashboard | AI Recommendations</title>
        <meta name="description" content="Track your learning progress and get personalized course recommendations" />
      </Head>

      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">Your Learning Dashboard</h1>
        
        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6" role="alert">
            <p>{error}</p>
          </div>
        )}

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6 flex items-center">
            <div className="rounded-full bg-blue-100 p-3 mr-4">
              <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p className="text-sm text-gray-500">Completed Courses</p>
              <p className="text-2xl font-bold text-gray-800">{learningData?.completedCourses || 0}</p>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6 flex items-center">
            <div className="rounded-full bg-green-100 p-3 mr-4">
              <svg className="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p className="text-sm text-gray-500">Learning Hours</p>
              <p className="text-2xl font-bold text-gray-800">{learningData?.totalHours || 0}</p>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6 flex items-center">
            <div className="rounded-full bg-yellow-100 p-3 mr-4">
              <svg className="w-8 h-8 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <p className="text-sm text-gray-500">Day Streak</p>
              <p className="text-2xl font-bold text-gray-800">{learningData?.streak || 0}</p>
            </div>
          </div>
        </div>

        {/* Learning Progress Chart */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Weekly Learning Progress</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart
                data={learningData?.progressData || progressData}
                margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area 
                  type="monotone" 
                  dataKey="completed" 
                  stroke="#8884d8" 
                  fill="#8884d8" 
                  fillOpacity={0.3} 
                  name="Completed Lessons"
                />
                <Area 
                  type="monotone" 
                  dataKey="target" 
                  stroke="#82ca9d" 
                  fill="#82ca9d" 
                  fillOpacity={0.3}
                  name="Target"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Skills and Learning Analytics */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Skills Progress</h2>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={learningData?.skillsData || skillsData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  >
                    {(learningData?.skillsData || skillsData).map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => `${value}%`} />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Learning Activity</h2>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={learningData?.progressData || progressData}
                  margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="completed" name="Completed Lessons" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Personalized Recommendations */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-gray-800">Recommended For You</h2>
            <a href="/courses" className="text-blue-600 hover:text-blue-800 text-sm font-medium">View All</a>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {recommendations.map((course) => (
              <div key={course.id} className="bg-white rounded-lg shadow overflow-hidden transition-transform duration-300 hover:transform hover:scale-105">
                <div className="h-40 bg-gray-200 relative">
                  <img 
                    src={course.image || 'https://via.placeholder.com/300x200'} 
                    alt={course.title}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="p-4">
                  <span className="text-xs font-semibold text-blue-600 uppercase tracking-wide">{course.category}</span>
                  <h3 className="mt-1 font-semibold text-gray-900 leading-tight truncate">{course.title}</h3>
                  <div className="mt-1 flex items-center">
                    <div className="flex items-center">
                      {[...Array(5)].map((_, i) => (
                        <svg 
                          key={i} 
                          className={`w-4 h-4 ${i < Math.floor(course.rating) ? 'text-yellow-400' : 'text-gray-300'}`} 
                          fill="currentColor" 
                          viewBox="0 0 20 20"
                        >
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                      ))}
                      <span className="ml-1 text-sm text-gray-600">{course.rating}</span>
                    </div>
                  </div>
                  <button className="mt-3 w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors">
                    View Course
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Trending Courses */}
        <div>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-gray-800">Trending Now</h2>
            <a href="/courses/trending" className="text-blue-600 hover:text-blue-800 text-sm font-medium">View All</a>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {topCourses.map((course) => (
              <div key={course.id} className="bg-white rounded-lg shadow overflow-hidden transition-transform duration-300 hover:transform hover:scale-105">
                <div className="h-40 bg-gray-200 relative">
                  <img 
                    src={course.image || 'https://via.placeholder.com/300x200'} 
                    alt={course.title}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute top-0 right-0 bg-yellow-400 text-xs font-bold px-2 py-1 m-2 rounded">
                    TRENDING
                  </div>
                </div>
                <div className="p-4">
                  <span className="text-xs font-semibold text-blue-600 uppercase tracking-wide">{course.category}</span>
                  <h3 className="mt-1 font-semibold text-gray-900 leading-tight truncate">{course.title}</h3>
                  <div className="mt-1 flex items-center">
                    <div className="flex items-center">
                      {[...Array(5)].map((_, i) => (
                        <svg 
                          key={i} 
                          className={`w-4 h-4 ${i < Math.floor(course.rating) ? 'text-yellow-400' : 'text-gray-300'}`} 
                          fill="currentColor" 
                          viewBox="0 0 20 20"
                        >
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                      ))}
                      <span className="ml-1 text-sm text-gray-600">{course.rating}</span>
                    </div>
                  </div>
                  <button className="mt-3 w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors">
                    View Course
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;