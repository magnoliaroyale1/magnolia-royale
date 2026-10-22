import {Container,Card,Button,Alert,Spinner} from 'react-bootstrap';
import {useSearchParams,useNavigate} from 'react-router-dom';
import {useApiResource} from '../hooks/useApi';
import type {CheckoutSession} from '../types';
import {PLANS} from '../utils/constants';
export function PaymentSuccess(){
 const [params]=useSearchParams();const id=params.get('session');const navigate=useNavigate();const {data,loading}=useApiResource<CheckoutSession|null>(id?`/checkouts/${id}`:null,null);
 return <Container className="py-5 mt-5"><Card className="border-0 shadow-sm mx-auto text-center" style={{maxWidth:600}}><Card.Body className="p-5">
 {loading?<Spinner animation="border"/>:data?.status==='completed'?<><i className="bi bi-check-circle text-olive display-3"/><h3 className="font-serif text-olive mt-3">Alteração demonstrativa concluída</h3><p>Plano {PLANS.find(p=>p.id===data.plan)?.name} ativo na base de demonstração.</p><p>Nenhuma cobrança foi realizada.</p></>:<Alert variant="warning">Não há uma alteração concluída para exibir.</Alert>}
 <Button variant="olive" className="rounded-pill" onClick={()=>navigate('/dashboard/clinic')}>Voltar ao painel</Button>
 </Card.Body></Card></Container>;
}
