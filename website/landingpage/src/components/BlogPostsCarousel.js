import React from 'react';
import Slider from 'react-slick';
import Card from './Card'

const BlogPostsCarousel = ({ posts }) => {
    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 1024, // Adjust breakpoint for vertical view
                settings: {
                    slidesToShow: 4,
                    slidesToScroll: 1,
                    infinite: true,
                    dots: true
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    initialSlide: 2
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
        ]
    };

    return (
        <div className='container mx-auto px-4 py-8'>
            <Slider {...settings}>
                {posts.slice(0, 5).map(post => (
                    <div key={post.id} className="container mx-auto flex flex-wrap justify-center">
                    <Card key={post.name} member={post} />
                    <div key={post.id} className="p-4">
                        <div className="max-w-md rounded overflow-hidden shadow-lg">
                            <div className="px-6 py-4">
                                <div className="font-bold text-xl mb-2">{post.title}</div>
                                <p className="text-gray-700 text-base">
                                    {post.summary}
                                </p>
                                <a href={post.link} className="text-blue-500">Read more</a>
                            </div>
                        </div>
                        </div>
                    </div>
                ))}
            </Slider>
        </div>
    );
};

export default BlogPostsCarousel;
