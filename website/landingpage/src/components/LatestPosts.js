import React, { useEffect, useState } from 'react';
import API from '../services/API';
import BlogPostsCarousel from './BlogPostsCarousel';
import LoadingBar from './LoadingBar';

const LatestPosts = () => {
    const [posts, setPosts] = useState([]);
    const [isLoading, setIsLoading] = useState(true);  // Add a loading state

    useEffect(() => {
        const fetchData = async () => {
            try {
                setIsLoading(true);  // Set loading to true before fetching data
                const response = await API.get('/posts');
                setPosts(response.data);  // Assume response is the array of posts
            } catch (error) {
                console.error('Error fetching data: ', error);
            } finally {
                setIsLoading(false);  // Set loading to false after fetching data
            }
        };

        fetchData();
    }, []);

    return (
        <div>
            {isLoading || posts.length === 0 ? <LoadingBar /> : <BlogPostsCarousel posts={posts} />}
        </div>
    );
};

export default LatestPosts;
