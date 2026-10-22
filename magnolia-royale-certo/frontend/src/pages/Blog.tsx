import { useState } from 'react';
import { Container, Row, Col, Card, Badge, Spinner } from 'react-bootstrap';
import { useBlogPosts } from '../hooks/useBlogPosts';
import { SEO } from '../components/SEO';
import { BlogArticleModal } from '../components/BlogArticleModal';
import { formatDateBR } from '../utils/date';
import type { BlogPost } from '../types';

export const Blog = () => {
  const { posts, loading } = useBlogPosts();
  const [selectedPost, setSelectedPost] = useState<BlogPost | null>(null);

  return (
    <Container className="py-5 mt-5">
      <SEO
        title="Blog"
        description="Dicas, tendências e guias sobre estética premium, procedimentos e cuidados com a pele."
        url="https://magnoliaroyale.com.br/blog"
      />
      <div className="text-center mb-5">
        <h2 className="font-serif fw-bold text-olive">Blog Magnolia Royale</h2>
        <p className="text-muted">Dicas e tendências do mundo da estética</p>
      </div>

      {loading ? (
        <div className="text-center py-5"><Spinner animation="border" className="text-olive" /></div>
      ) : posts.length === 0 ? (
        <div className="text-center py-5">
          <i className="bi bi-newspaper text-muted fs-1 d-block mb-3"></i>
          <p className="text-muted">Nenhum post publicado ainda.</p>
        </div>
      ) : (
        <Row className="g-4">
          {posts.map(post => (
            <Col md={6} key={post.id}>
              <Card
                className="border-0 shadow-sm card-hover h-100"
                role="button"
                tabIndex={0}
                aria-label={`Ler artigo: ${post.title} — ${post.clinicName || post.author}`}
                style={{ cursor: 'pointer' }}
                onClick={() => setSelectedPost(post)}
                onKeyDown={event => {
                  if (event.key === 'Enter' || event.key === ' ') {
                    event.preventDefault();
                    setSelectedPost(post);
                  }
                }}
              >
                <Card.Img
                  src={post.image || '/clinic-demo.svg'}
                  alt={`Imagem do artigo ${post.title}`}
                  style={{ height: '250px', objectFit: 'cover' }}
                />
                <Card.Body className="p-4">
                  {post.category && (
                    <Badge bg="light" text="dark" className="mb-2">{post.category}</Badge>
                  )}
                  <h4 className="font-serif fw-bold text-olive mb-2">{post.title}</h4>
                  <p className="text-muted mb-2">{post.excerpt}</p>
                  {(post.clinicName || post.author) && (
                    <small className="text-muted d-block mb-3">Por {post.clinicName || post.author}</small>
                  )}
                  <div className="d-flex justify-content-between align-items-center">
                    <small className="text-muted">
                      <i className="bi bi-clock me-1"></i>
                      {post.readTime} min de leitura
                    </small>
                    <small className="text-muted">
                      {formatDateBR(post.createdAt)}
                    </small>
                  </div>
                  <span className="text-olive fw-semibold small d-block mt-3">Ler artigo <i className="bi bi-arrow-right ms-1"></i></span>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      )}

      <BlogArticleModal post={selectedPost} onClose={() => setSelectedPost(null)} />
    </Container>
  );
};
