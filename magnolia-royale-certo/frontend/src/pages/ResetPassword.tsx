import {useState} from 'react';
import {Container,Card,Form,Button,Alert} from 'react-bootstrap';
import {Link,useSearchParams} from 'react-router-dom';
import {api} from '../services/api';
export function ResetPassword(){
 const [params]=useSearchParams();const [password,setPassword]=useState('');const [confirm,setConfirm]=useState('');const [done,setDone]=useState(false);const [busy,setBusy]=useState(false);const [error,setError]=useState('');
 return <Container className="py-5 mt-5"><Card className="border-0 shadow-sm mx-auto" style={{maxWidth:480}}><Card.Body className="p-4"><h3 className="font-serif text-olive">Redefinir senha</h3>
 {done?<Alert variant="success">Senha alterada. <Link to="/login">Entrar na conta</Link></Alert>:<Form onSubmit={async e=>{e.preventDefault();if(password!==confirm){setError('As senhas não conferem.');return;}setBusy(true);try{await api('/auth/reset','POST',{token:params.get('token'),password});setDone(true);}catch(e){setError((e as Error).message);}finally{setBusy(false);}}}>
 {error&&<Alert variant="danger">{error}</Alert>}
 <Form.Group className="my-3" controlId="new-password"><Form.Label>Nova senha</Form.Label><Form.Control type="password" minLength={8} required value={password} onChange={e=>setPassword(e.target.value)}/></Form.Group>
 <Form.Group className="my-3" controlId="confirm-password"><Form.Label>Confirme a senha</Form.Label><Form.Control type="password" minLength={8} required value={confirm} onChange={e=>setConfirm(e.target.value)}/></Form.Group>
 <Button type="submit" variant="olive" disabled={busy} className="rounded-pill">Salvar nova senha</Button></Form>}
 </Card.Body></Card></Container>;
}
