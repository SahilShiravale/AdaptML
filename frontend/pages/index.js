import { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import Image from 'next/image';
import { useRouter } from 'next/router';

// Placeholder for WebSocket connection
let socket;

export default function Home() {
  const router = useRouter();
  const [topPicks, setTopPicks] = useState([]);
  const [trending, setTrending] = useState([]);
  const [aiSuggestions, setAiSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [chatbotOpen, setChatbotOpen] = useState(false);
  const [notifications, setNotifications] = useState([]);

  // Fetch initial data
  useEffect(() => {
    const fetchData = async () => {
      try {
        // In a real app, these would be API calls
        const topPicksResponse = await mockFetchTopPicks();
        const trendingResponse = await mockFetchTrending();
        const aiSuggestionsResponse = await mockFetchAiSuggestions();
        
        setTopPicks(topPicksResponse);
        setTrending(trendingResponse);
        setAiSuggestions(aiSuggestionsResponse);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  // Setup WebSocket connection for real-time updates
  useEffect(() => {
    // Initialize WebSocket connection
    socket = new WebSocket(process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws');
    
    socket.onopen = () => {
      console.log('WebSocket connection established');
    };
    
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      // Handle different types of real-time updates
      switch (data.type) {
        case 'new_recommendation':
          setAiSuggestions(prev => [data.course, ...prev].slice(0, 10));
          setNotifications(prev => [...prev, { 
            id: Date.now(), 
            message: `New recommendation: ${data.course.title}` 
          }]);
          break;
        case 'trending_update':
          setTrending(data.courses);
          break;
        default:
          console.log('Received unknown update type:', data.type);
      }
    };
    
    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    socket.onclose = () => {
      console.log('WebSocket connection closed');
    };
    
    // Clean up WebSocket connection on component unmount
    return () => {
      if (socket && socket.readyState === WebSocket.OPEN) {
        socket.close();
      }
    };
  }, []);

  // Mock data fetching functions (would be replaced with actual API calls)
  const mockFetchTopPicks = async () => {
    return [
      { id: 1, title: 'Machine Learning Fundamentals', image: '/images/course1.jpg', rating: 4.8, students: 12500, price: 49.99 },
      { id: 2, title: 'Advanced React Patterns', image: '/images/course2.jpg', rating: 4.9, students: 8300, price: 59.99 },
      { id: 3, title: 'Data Science with Python', image: '/images/course3.jpg', rating: 4.7, students: 15200, price: 44.99 },
      { id: 4, title: 'Full Stack Web Development', image: '/images/course4.jpg', rating: 4.6, students: 10800, price: 69.99 },
      { id: 5, title: 'iOS App Development with Swift', image: '/images/course5.jpg', rating: 4.5, students: 7600, price: 54.99 },
    ];
  };

  const mockFetchTrending = async () => {
    return [
      { id: 6, title: 'Blockchain Development', image: '/images/course6.jpg', rating: 4.7, students: 9200, price: 64.99 },
      { id: 7, title: 'UX/UI Design Principles', image: '/images/course7.jpg', rating: 4.8, students: 11300, price: 49.99 },
      { id: 8, title: 'Cloud Computing with AWS', image: '/images/course8.jpg', rating: 4.6, students: 8700, price: 59.99 },
      { id: 9, title: 'Cybersecurity Fundamentals', image: '/images/course9.jpg', rating: 4.9, students: 13400, price: 74.99 },
      { id: 10, title: 'Digital Marketing Mastery', image: '/images/course10.jpg', rating: 4.5, students: 10100, price: 44.99 },
    ];
  };

  const mockFetchAiSuggestions = async () => {
    return [
      { id: 11, title: 'Natural Language Processing', image: '/images/course11.jpg', rating: 4.8, students: 7800, price: 69.99, match: 98 },
      { id: 12, title: 'DevOps Engineering', image: '/images/course12.jpg', rating: 4.7, students: 9100, price: 64.99, match: 95 },
      { id: 13, title: 'Mobile App Design', image: '/images/course13.jpg', rating: 4.6, students: 6500, price: 49.99, match: 92 },
      { id: 14, title: 'Game Development with Unity', image: '/images/course14.jpg', rating: 4.9, students: 12200, price: 79.99, match: 90 },
      { id: 15, title: 'Business Intelligence', image: '/images/course15.jpg', rating: 4.5, students: 8400, price: 54.99, match: 87 },
    ];
  };

  // Course Card Component
  const CourseCard = ({ course, isAiSuggestion = false }) => (
    <div className="flex flex-col bg-white rounded-lg shadow-md overflow-hidden transition-transform duration-300 hover:scale-105 hover:shadow-xl">
      <div className="relative h-40 w-full">
        <div className="absolute inset-0 bg-gray-200 animate-pulse"></div>
        {/* In a real app, this would be an actual image */}
        {/* <Image src={course.image} alt={course.title} layout="fill" objectFit="cover" /> */}
      </div>
      <div className="p-4 flex-grow">
        <h3 className="text-lg font-semibold text-gray-800 line-clamp-2">{course.title}</h3>
        <div className="flex items-center mt-2">
          <div className="flex text-yellow-400">
            {[...Array(5)].map((_, i) => (
              <svg key={i} className={`w-4 h-4 ${i < Math.floor(course.rating) ? 'fill-current' : 'text-gray-300'}`} viewBox="0 0 20 20">
                <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z" />
              </svg>
            ))}
            <span className="ml-1 text-sm text-gray-600">{course.rating}</span>
          </div>
          <span className="ml-2 text-sm text-gray-500">({course.students.toLocaleString()} students)</span>
        </div>
        <div className="mt-3 flex justify-between items-center">
          <span className="font-bold text-gray-900">${course.price}</span>
          {isAiSuggestion && (
            <span className="bg-green-100 text-green-800 text-xs font-medium px-2 py-1 rounded">
              {course.match}% Match
            </span>
          )}
        </div>
      </div>
      <div className="px-4 pb-4">
        <button 
          onClick={() => router.push(`/course/${course.id}`)}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded transition-colors duration-300"
        >
          View Course
        </button>
      </div>
    </div>
  );

  // Carousel Component
  const Carousel = ({ title, courses, isAiSuggestion = false }) => (
    <div className="my-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">{title}</h2>
      <div className="relative">
        <div className="flex overflow-x-auto pb-4 hide-scrollbar space-x-4">
          {courses.map(course => (
            <div key={course.id} className="flex-none w-64">
              <CourseCard course={course} isAiSuggestion={isAiSuggestion} />
            </div>
          ))}
        </div>
        <button className="absolute left-0 top-1/2 transform -translate-y-1/2 bg-white rounded-full p-2 shadow-md z-10 hover:bg-gray-100">
          <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <button className="absolute right-0 top-1/2 transform -translate-y-1/2 bg-white rounded-full p-2 shadow-md z-10 hover:bg-gray-100">
          <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>
  );

  // Chatbot Widget
  const ChatbotWidget = () => (
    <div className={`fixed bottom-6 right-6 z-50 transition-all duration-300 ${chatbotOpen ? 'scale-100' : 'scale-0'}`}>
      <div className="bg-white rounded-lg shadow-xl w-80 h-96 flex flex-col overflow-hidden">
        <div className="bg-blue-600 text-white p-4 flex justify-between items-center">
          <h3 className="font-medium">Learning Assistant</h3>
          <button onClick={() => setChatbotOpen(false)} className="text-white hover:text-gray-200">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div className="flex-grow p-4 bg-gray-50 overflow-y-auto">
          <div className="bg-blue-100 rounded-lg p-3 mb-3 max-w-[80%]">
            <p className="text-sm">Hi there! I'm your AI learning assistant. How can I help you find the perfect course today?</p>
          </div>
          {/* Chat messages would go here */}
        </div>
        <div className="p-4 border-t">
          <div className="flex">
            <input 
              type="text" 
              placeholder="Type your message..." 
              className="flex-grow border rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button className="bg-blue-600 text-white px-4 py-2 rounded-r-lg hover:bg-blue-700">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  // Chatbot Toggle Button
  const ChatbotToggle = () => (
    <button 
      onClick={() => setChatbotOpen(!chatbotOpen)} 
      className={`fixed bottom-6 right-6 z-50 bg-blue-600 text-white rounded-full p-4 shadow-lg hover:bg-blue-700 transition-all duration-300 ${chatbotOpen ? 'scale-0' : 'scale-100'}`}
    >
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
      </svg>
    </button>
  );

  // Notification Toast
  const NotificationToast = ({ notification, onClose }) => (
    <div className="fixed top-4 right-4 bg-white rounded-lg shadow-lg p-4 flex items-center z-50 animate-slideIn">
      <div className="bg-blue-100 rounded-full p-2 mr-3">
        <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <div className="flex-grow">
        <p className="text-sm font-medium text-gray-900">{notification.message}</p>
      </div>
      <button onClick={onClose} className="ml-4 text-gray-400 hover:text-gray-500">
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  );

  // Remove notification after 5 seconds
  useEffect(() => {
    if (notifications.length > 0) {
      const timer = setTimeout(() => {
        setNotifications(prev => prev.slice(1));
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [notifications]);

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>AI Learning Platform - Personalized Course Recommendations</title>
        <meta name="description" content="Discover courses tailored to your learning style and goals with our AI-powered recommendation system" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* Header would typically be a separate component */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <Link href="/">
                <a className="flex items-center">
                  <span className="text-2xl font-bold text-blue-600">LearnSmart</span>
                </a>
              </Link>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/dashboard">
                <a className="text-gray-600 hover:text-gray-900">Dashboard</a>
              </Link>
              <Link href="/courses">
                <a className="text-gray-600 hover:text-gray-900">Courses</a>
              </Link>
              <Link href="/login">
                <a className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md">Sign In</a>
              </Link>
            </div>
          </div>
        </div>
      </header>

      <main>
        {/* Hero Section */}
        <section className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
              <div>
                <h1 className="text-4xl md:text-5xl font-extrabold leading-tight">
                  Discover Your Perfect Learning Path
                </h1>
                <p className="mt-4 text-xl text-blue-100">
                  Our AI-powered platform analyzes your learning style, goals, and preferences to recommend courses that match your unique needs.
                </p>
                <div className="mt-8 flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
                  <button className="bg-white text-blue-700 hover:bg-blue-50 px-6 py-3 rounded-md font-medium text-lg transition-colors duration-300">
                    Get Started
                  </button>
                  <button className="bg-transparent border-2 border-white text-white hover:bg-white hover:text-blue-700 px-6 py-3 rounded-md font-medium text-lg transition-colors duration-300">
                    Take Assessment
                  </button>
                </div>
              </div>
              <div className="hidden md:block relative h-80">
                {/* Placeholder for hero image */}
                <div className="absolute inset-0 bg-blue-400 bg-opacity-30 rounded-lg"></div>
              </div>
            </div>
          </div>
        </section>

        {/* Main Content */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {isLoading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-600"></div>
            </div>
          ) : (
            <>
              {/* AI-Generated Suggestions */}
              <Carousel 
                title="AI-Powered Recommendations for You" 
                courses={aiSuggestions} 
                isAiSuggestion={true} 
              />
              
              {/* Top Picks Carousel */}
              <Carousel 
                title="Top Picks for You" 
                courses={topPicks} 
              />
              
              {/* Trending Now Carousel */}
              <Carousel 
                title="Trending Now" 
                courses={trending} 
              />
              
              {/* Learning Path Section */}
              <section className="my-16 bg-gray-100 rounded-xl p-8">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                  <div>
                    <h2 className="text-3xl font-bold text-gray-800">Personalized Learning Paths</h2>
                    <p className="mt-4 text-gray-600">
                      Our AI doesn't just recommend individual courses—it creates customized learning paths to help you achieve your career goals step by step.
                    </p>
                    <button className="mt-6 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-md font-medium transition-colors duration-300">
                      Explore Learning Paths
                    </button>
                  </div>
                  <div className="relative h-64">
                    {/* Placeholder for learning path illustration */}
                    <div className="absolute inset-0 bg-gray-300 rounded-lg"></div>
                  </div>
                </div>
              </section>
            </>
          )}
        </div>
      </main>

      {/* Footer would typically be a separate component */}
      <footer className="bg-gray-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-4">LearnSmart</h3>
              <p className="text-gray-400">
                AI-powered learning platform with personalized course recommendations.
              </p>
            </div>
            <div>
              <h4 className="font-medium mb-4">Explore</h4>
              <ul className="space-y-2">
                <li><Link href="/courses"><a className="text-gray-400 hover:text-white">All Courses</a></Link></li>
                <li><Link href="/learning-paths"><a className="text-gray-400 hover:text-white">Learning Paths</a></Link></li>
                <li><Link href="/instructors"><a className="text-gray-400 hover:text-white">Instructors</a></Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium mb-4">Resources</h4>
              <ul className="space-y-2">
                <li><Link href="/blog"><a className="text-gray-400 hover:text-white">Blog</a></Link></li>
                <li><Link href="/help"><a className="text-gray-400 hover:text-white">Help Center</a></Link></li>
                <li><Link href="/faq"><a className="text-gray-400 hover:text-white">FAQ</a></Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium mb-4">Connect</h4>
              <ul className="space-y-2">
                <li><Link href="/contact"><a className="text-gray-400 hover:text-white">Contact Us</a></Link></li>
                <li><a href="#" className="text-gray-400 hover:text-white">Twitter</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white">LinkedIn</a></li>
              </ul>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-700 text-center text-gray-400">
            <p>&copy; {new Date().getFullYear()} LearnSmart. All rights reserved.</p>
          </div>
        </div>
      </footer>

      {/* Chatbot */}
      <ChatbotWidget />
      <ChatbotToggle />

      {/* Notifications */}
      {notifications.map((notification, index) => (
        <NotificationToast 
          key={notification.id} 
          notification={notification} 
          onClose={() => setNotifications(prev => prev.filter(n => n.id !== notification.id))} 
        />
      ))}

      {/* Custom styles */}
      <style jsx>{`
        .hide-scrollbar::-webkit-scrollbar {
          display: none;
        }
        .hide-scrollbar {
          -ms-overflow-style: none;
          scrollbar-width: none;
        }
        @keyframes slideIn {
          from { transform: translateX(100%); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
        .animate-slideIn {
          animation: slideIn 0.3s ease-out forwards;
        }
      `}</style>
    </div>
  );
}