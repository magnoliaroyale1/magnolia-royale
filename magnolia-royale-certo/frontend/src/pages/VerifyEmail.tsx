import {useEffect,useRef,useState} from 'react';
import {Container,Card,Button,Alert,Spinner} from 'react-bootstrap';
import {Link,useSearchParams,useNavigate} from 'react-router-dom';
import {useAuth} from '../context/AuthContext';
import {api} from '../services/api';
export function VerifyEmail(){
 const {user,demoMode,refreshUser,sendVerificationEmail,logout}=useAuth();
 const [params]=useSearchParams();const token=params.get('token');const processed=useRef(false);
 const [message,setMessage]=useState('');const [busy,setBusy]=useState(false);const navigate=useNavigate();
 useEffect(()=>{if(user?.emailVerified)navigate(`/dashboard/${user.role}`,{replace:true});},[user,navigate]);
 useEffect(()=>{if(!token||processed.current)return;processed.current=true;setBusy(true);
  api('/auth/verify','POST',{token}).then(async()=>{setMessage('E-mail confirmado. Sua conta está pronta.');await refreshUser();}).catch(e=>setMessage(e.message)).finally(()=>setBusy(false));
 },[token,refreshUser]);
 return <Container className="py-5 mt-5"><Card className="border-0 shadow-sm mx-auto" style={{maxWidth:540}}><Card.Body className="p-5 text-center">
  <i className="bi bi-envelope-check text-olive display-3"/><h3 className="font-serif text-olive mt-3">Confirme seu e-mail</h3>
  <p>Abra o link enviado para {user?.email||'seu e-mail'} para ativar sua conta.</p>
  {message&&<Alert variant="info">{message}</Alert>}{busy&&<Spinner animation="border"/>}
  <div className="d-grid gap-2 mt-3">
   {demoMode&&<Link to="/demo-mailbox" className="btn btn-olive rounded-pill">Abrir caixa de e-mails da demonstração</Link>}
   {user&&<><Button variant="outline-olive" className="rounded-pill" onClick={()=>refreshUser().then(u=>setMessage(u?.emailVerified?'E-mail confirmado.':'A confirmação ainda está pendente.')).catch(()=>{})}>Já confirmei, verificar</Button>
    <Button variant="link" onClick={()=>sendVerificationEmail().then(()=>setMessage('Link reenviado.')).catch(()=>{})}>Reenviar e-mail</Button><Button variant="link" onClick={logout}>Sair</Button></>}
   {!user&&<Link to="/login">Entrar na conta</Link>}
  </div>
 </Card.Body></Card></Container>;
}
