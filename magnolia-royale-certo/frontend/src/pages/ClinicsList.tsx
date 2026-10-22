import {useApiResource} from '../hooks/useApi';
import {queryString} from '../services/api';
import { useState, useEffect } from 'react';
import { Container, Row, Col, Spinner, Button } from 'react-bootstrap';
import { ClinicCard } from '../components/ClinicCard';
import { SearchFilters } from '../components/SearchFilters';
import { useFavorites } from '../hooks/useFavorites';
import { SEO } from '../components/SEO';
import { useAuth } from '../context/AuthContext';
import { useSearchHistory } from '../hooks/useSearchHistory';
import type { Clinic } from '../types';

interface Filters {
  location: string;
  procedure: string;
  minPrice: string;
  maxPrice: string;
  minRating: string;
  verifiedOnly: boolean;
}

export const ClinicsList = () => {
  const { user } = useAuth();
  const { saveSearch } = useSearchHistory(user?.uid || '');

  const [filters,setFilters]=useState<Record<string,string|boolean>>({});
  const [displayLimit,setDisplayLimit]=useState(9);
  const {data:filteredClinics,loading}=useApiResource<Clinic[]>('/clinics?'+queryString(filters),[]);
  const handleFilter=(next:Filters)=>{
    setFilters({...next});setDisplayLimit(9);
    if(user) void saveSearch('',{location:next.location,procedure:next.procedure,minRating:next.minRating,verifiedOnly:next.verifiedOnly?'sim':''});
  };

  return (
    <Container className="py-5 mt-5">
      <SEO
        title="Encontrar Clínicas"
        description="Explore e compare as melhores clínicas de estética premium. Filtre por localização, procedimento e avaliação."
        url="https://magnoliaroyale.com.br/clinics"
      />
      <div className="mb-4">
        <h2 className="font-serif fw-bold text-olive">Encontre sua Clínica</h2>
        <p className="text-muted">Explore as melhores clínicas de estética premium</p>
      </div>

      <SearchFilters onFilter={handleFilter} />

      {loading ? (
        <div className="text-center py-5">
          <Spinner animation="border" className="text-olive" />
        </div>
      ) : filteredClinics.length === 0 ? (
        <div className="text-center py-5">
          <i className="bi bi-search text-muted fs-1 mb-3 d-block"></i>
          <p className="text-muted">Nenhuma clínica encontrada com esses filtros.</p>
        </div>
      ) : (
        <>
          <Row className="g-4">
            {filteredClinics.slice(0, displayLimit).map(clinic => (
              <Col md={6} lg={4} key={clinic.id}>
                <ClinicCard clinic={clinic} />
              </Col>
            ))}
          </Row>
          {displayLimit < filteredClinics.length && (
            <div className="text-center mt-4">
              <Button variant="outline-olive" className="rounded-pill px-5" onClick={() => setDisplayLimit(prev => prev + 9)}>
                Carregar mais ({filteredClinics.length - displayLimit} restantes)
              </Button>
            </div>
          )}
        </>
      )}
    </Container>
  );
};
