import {useState} from 'react';
import {Container,Card,Form,Button,Alert} from 'react-bootstrap';
import {useSearchParams,useNavigate} from 'react-router-dom';
import {useAuth} from '../context/AuthContext';
import {useCheckout} from '../hooks/useCheckout';
import {PLANS} from '../utils/constants';
export function Checkout(){
 const {user,demoMode}=useAuth();const [params]=useSearchParams();const navigate=useNavigate();
 const plan=PLANS.find(p=>p.id===params.get('plan'))||PLANS[0];
 const [method,setMethod]=useState<'credit_card'|'boleto'|'pix'>('pix');
 const {createCheckoutSession,completeCheckout,processing}=useCheckout();
 return <Container className="py-5 mt-5"><Card className="border-0 shadow-sm mx-auto" style={{maxWidth:600}}><Card.Body className="p-5">
 <h3 className="font-serif text-olive">Plano {plan.name}</h3><p className="fs-4 text-olive">R$ {plan.price},00 / mês</p>
 <Alert variant="info">Demonstração acadêmica: esta operação altera o plano na base de testes e não realiza cobranças.</Alert>
 <Form.Group controlId="payment-method" className="mb-4"><Form.Label>Forma de pagamento demonstrativa</Form.Label><Form.Select value={method} onChange={e=>setMethod(e.target.value as typeof method)}><option value="pix">Pix</option><option value="boleto">Boleto</option><option value="credit_card">Cartão</option></Form.Select></Form.Group>
 <Button variant="gold" disabled={processing||!demoMode} className="rounded-pill" onClick={async()=>{if(!user?.clinicId)return;const id=await createCheckoutSession(user.clinicId,plan.id as any,plan.price);if(id&&await completeCheckout(user.clinicId,id,method))navigate(`/dashboard/clinic/checkout/sucesso?session=${id}`);}}>{processing?'Salvando...':'Confirmar alteração demonstrativa'}</Button>
 </Card.Body></Card></Container>;
}
