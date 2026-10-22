interface StarRatingProps {
    rating: number;
    maxRating?: number;
    size?: 'sm' | 'md' | 'lg';
    interactive?: boolean;
    onRate?: (rating: number) => void;
  }
  
  export const StarRating = ({ 
    rating, 
    maxRating = 5, 
    size = 'md', 
    interactive = false,
    onRate 
  }: StarRatingProps) => {
    const sizeClass = size === 'sm' ? 'fs-6' : size === 'lg' ? 'fs-3' : 'fs-5';
    
    const handleClick = (index: number) => {
      if (interactive && onRate) {
        onRate(index + 1);
      }
    };
  
    return (
      <div className="d-flex gap-1">
        {[...Array(maxRating)].map((_, index) => (
          interactive ? <button type="button" key={index}
            aria-label={`${index + 1} estrela${index ? 's' : ''}`} aria-pressed={index < rating}
            className="border-0 bg-transparent p-0" onClick={() => handleClick(index)}>
            <i className={`bi ${index < rating ? 'bi-star-fill text-gold' : 'bi-star text-muted'} ${sizeClass}`} />
          </button> : <i key={index}
            className={`bi ${index < rating ? 'bi-star-fill text-gold' : 'bi-star text-muted'} ${sizeClass}`} />
        ))}
      </div>
    );
  };
