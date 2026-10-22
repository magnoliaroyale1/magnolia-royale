import {Container,Card,Spinner,Alert} from 'react-bootstrap';
import {Link,useParams} from 'react-router-dom';
import {useApiResource} from '../../hooks/useApi';
import type {AssessmentData} from '../../hooks/useClinicAssessment';
export function AssessmentReview(){const{id}=useParams();const{data,loading}=useApiResource<AssessmentData|null>(id?`/clinics/${id}/assessment`:null,null);
return <Container className="py-5 mt-5" style={{maxWidth:850}}><Link to="/dashboard/admin/approval">Voltar às aprovações</Link><h2 className="font-serif text-olive my-3">Questionário da clínica</h2>{loading?<Spinner animation="border"/>:!data?<Alert variant="info">Questionário ainda não enviado.</Alert>:<>
<Card className="mb-3"><Card.Body><h5>Documentação</h5>{([['cnpjFile','CNPJ'],['alvaraFile','Alvará'],['licencaSanitaria','Licença sanitária']] as const).map(([key,label])=><p key={key}>{label}: {data.documentacao[key]?<a href={data.documentacao[key]} target="_blank" rel="noreferrer">Abrir documento</a>:'Não enviado'}</p>)}<p>Registro: {data.documentacao.registroVigilancia}</p></Card.Body></Card>
<Card className="mb-3"><Card.Body><h5>Profissionais informados</h5>{data.profissionais.lista.map((p,i)=><p key={i}>{p.nome} — {p.certificacao} {p.certificadoFile&&<a href={p.certificadoFile} target="_blank" rel="noreferrer">Certificado</a>}</p>)}</Card.Body></Card>
<Card className="mb-3"><Card.Body><h5>Estrutura e horários</h5><p>{data.estrutura.equipamentos.join(', ')}</p><p>{data.estrutura.metragem} m²</p><p>{data.horarios.diasSemana.join(', ')}: {data.horarios.abertura} às {data.horarios.fechamento}</p>{data.estrutura.fotos.map(url=><img alt="Estrutura da clínica" key={url} src={url} style={{width:200,margin:8}}/>)}</Card.Body></Card></>}</Container>;}
