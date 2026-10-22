import {Container,Card,Button,Alert} from 'react-bootstrap';
import {Link} from 'react-router-dom';
import {useApiResource} from '../hooks/useApi';
interface Mail{to:string;subject:string;body:string;link:string;createdAt:Date;}
export function DemoMailbox(){
 const {data,loading,refetch}=useApiResource<Mail[]>('/auth/mailbox',[],true);
 return <Container className="py-5 mt-5" style={{maxWidth:850}}><h2 className="font-serif text-olive">E-mails da demonstração</h2>
 <Alert variant="info">Caixa local para contas fictícias. Os links de confirmação e recuperação de senha aparecem aqui.</Alert>
 <Button variant="outline-olive" onClick={refetch} className="mb-3 rounded-pill">Atualizar caixa</Button>
 {!loading&&!data.length&&<p>Nenhuma mensagem recebida. Cadastre uma conta ou solicite um novo link.</p>}
 {data.map((mail,index)=><Card key={index} className="border-0 shadow-sm mb-3"><Card.Body><small>{mail.to}</small><h5 className="mt-2">{mail.subject}</h5><p>{mail.createdAt.toLocaleString('pt-BR')}</p>{mail.link?<Link className="btn btn-olive rounded-pill" to={new URL(mail.link).pathname+new URL(mail.link).search}>Abrir link recebido</Link>:<p>{mail.body}</p>}</Card.Body></Card>)}
 <Link to="/login">Voltar para o login</Link></Container>;
}
