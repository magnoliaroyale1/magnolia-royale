import { Badge, Button, Modal } from 'react-bootstrap';
import type { BlogPost } from '../types';
import { formatDateBR } from '../utils/date';

interface BlogArticleModalProps {
  post: BlogPost | null;
  onClose: () => void;
}

/** Exibe o texto integral que já é retornado pela API /blog. */
export const BlogArticleModal = ({ post, onClose }: BlogArticleModalProps) => (
  <Modal show={post !== null} onHide={onClose} centered size="lg" scrollable>
    <Modal.Header closeButton>
      <Modal.Title className="font-serif text-olive">{post?.title}</Modal.Title>
    </Modal.Header>
    {post && (
      <>
        <Modal.Body>
          <img
            src={post.image || '/clinic-demo.svg'}
            alt={`Imagem do artigo ${post.title}`}
            className="w-100 rounded-3 mb-3"
            style={{ maxHeight: '320px', objectFit: 'cover' }}
          />
          <div className="d-flex flex-wrap align-items-center gap-2 mb-3">
            {post.category && <Badge bg="light" text="dark">{post.category}</Badge>}
            <small className="text-muted">{post.readTime} min de leitura</small>
            <small className="text-muted">{formatDateBR(post.createdAt)}</small>
          </div>
          {(post.clinicName || post.author) && (
            <p className="text-muted small mb-3">
              Publicado por {post.clinicName || post.author}
            </p>
          )}
          {post.excerpt && <p className="fw-semibold text-olive">{post.excerpt}</p>}
          <p className="mb-0" style={{ whiteSpace: 'pre-wrap', overflowWrap: 'anywhere' }}>
            {post.content || 'O conteúdo deste artigo ainda não está disponível.'}
          </p>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="outline-secondary" className="rounded-pill" onClick={onClose}>
            Fechar artigo
          </Button>
        </Modal.Footer>
      </>
    )}
  </Modal>
);
