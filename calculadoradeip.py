
class Ip:
    def __init__(self, ip, cidr):
        
        self.ip = ip
        self.cidr = int(cidr)
        self.tipo = 'CLASSLESS'


    def to_ip(self, conj: str):
        """Converte um IP binário para o formato decimal

        Args:
            conj (str): IP em formato binário

        Returns:
            str: IP formatado em decimal com separação por ponto
        """
        
        conj = conj.split('.')
        bin = [128, 64, 32, 16, 8, 4, 2, 1]
        n_ip = ''
        
        for oct in conj:
            n = 0
            
            for x, y in zip(oct, bin):
                if x == '1':
                    n += y
                    
            n_ip += f'{n}.'
        n_ip = n_ip[:-1]
        
        return n_ip
    
    def to_bin(self, oct: str):
        """Converte um IP do formato decimal para o binário

        Args:
            oct (str): IP em formato decimal

        Returns:
            str: IP em formato binário
        """
        
        n_ip = oct.split('.')
        ip_bin = ''
        bin = [128, 64, 32, 16, 8, 4, 2, 1]
        
        for x in n_ip:
            calc = int(x)
            
            for y in bin:
                if calc - y >= 0:
                    ip_bin += '1'
                    calc -= y
                else:
                    ip_bin += '0'
                                
            ip_bin += '.'
        ip_bin = ip_bin[:-1]
        
        return ip_bin
    
    @property
    def ip_bin(self):
        return self.to_bin(self.ip)

    @property
    def sub_bin(self):
        """Calcula a submáscara de rede binária com base no CIDR

        Returns:
            str: Submáscara de rede no formato binário
        """
        
        sub_bin = ''
        for x in range(self.cidr):
            sub_bin += '1'
        
        while len(sub_bin) < 32:
            sub_bin += '0'
        
        sub_bin = f'{sub_bin[0:8]}.{sub_bin[8:16]}.{sub_bin[16:24]}.\
            {sub_bin[24:]}'.replace(' ', '')
            
        return sub_bin
    
    @property
    def sub(self):
        return self.to_ip(self.sub_bin)
    
    @property
    def host(self):
        """Calcula a quantidade de possíveis hosts

        Returns:
            int: Número de hosts possíveis
        """

        cont = 0
        for x in self.sub_bin:
            if x == '0':
                cont += 1

        return (2 ** cont) - 2

    @property
    def rede(self):
        """Calcula de forma binária o primeiro endereço da rede

        Returns:
            str: Primeiro endereço da rede
        """

        ip_bin = self.ip_bin.replace('.', '')
        bits_host = 32 - self.cidr
        ip_rede = ip_bin[: - bits_host]
        
        for index, bit in enumerate(ip_bin):
            if index + 1 > self.cidr:
                ip_rede = ip_rede + '0'

        ip_rede_separado = f"{ip_rede[0:8]}.{ip_rede[8:16]}.{ip_rede[16:24]}.\
            {ip_rede[24:]}".replace(' ', '')

        return self.to_ip(ip_rede_separado)
    
    @property
    def broadcast(self):
        """Calcula de forma binária o último endereço da rede

        Returns:
            str: Último endereço/broadcast
        """

        ip_bin = self.ip_bin.replace('.', '')
        bits_host = 32 - self.cidr
        ip_broadcast = ip_bin[: - bits_host]
        
        for index, bit in enumerate(ip_bin):
            if index + 1 > self.cidr:
                ip_broadcast = ip_broadcast + '1'

        ip_broadcast_separado = f"{ip_broadcast[0:8]}.{ip_broadcast[8:16]}.\
            {ip_broadcast[16:24]}.{ip_broadcast[24:]}".replace(' ', '')
            
        return self.to_ip(ip_broadcast_separado)
    
    @property
    def primeiro_ip_util(self):
        """ Primeiro IP que pode ser realmente atribuído pela rede """

        rede = self.rede.split('.')
        ip_util = int(rede[3]) + 1
        return f'{rede[0]}.{rede[1]}.{rede[2]}.{ip_util}'
    
    @property
    def ultimo_ip_util(self):
        """ Último IP que pode ser realmente atribuído pela rede """

        broadcast = self.broadcast.split('.')
        ip_util = int(broadcast[3]) - 1
        return f'{broadcast[0]}.{broadcast[1]}.{broadcast[2]}.{ip_util}'
    
    @property
    def classe(self):
        """ Encontra a classe do IP e se a máscara de rede estiver de acordo com
        a classe, reconhece como uma POSSÍVEL rede classfull """

        ip = self.ip.split('.')
        if int(ip[0]) <= 127:
            if self.cidr == 8:
                self.tipo = 'CLASSFULL'
            classe = 'A'
        
        elif int(ip[0]) <= 191:
            if self.cidr == 16:
                self.tipo = 'CLASSFULL'
            classe = 'B'

        elif int(ip[0]) <= 223:
            if self.cidr == 24:
                self.tipo = 'CLASSFULL'
            classe = 'C'

        elif int(ip[0]) <= 239:
            classe = 'D'

        elif int(ip[0]) <= 255:
            classe = 'E'
        
        else:
            raise Exception('IP inválido')
        return classe


    
if __name__ == "__main__":
    
    ip = input('Digite o IP com pontos inclusos: ')
    cidr = input('Digite o cidr da máscara de sub-rede: ')

    ip1 = Ip(ip, int(cidr))

    print(f'\n\n\nClasse: {ip1.classe}')
    print(f'Tipo: {ip1.tipo}')
    print(f'Ip: {ip1.ip}')
    print(f'Máscara de sub-rede: {ip1.sub}')
    print(f'Hosts possíveis: {ip1.host}')
    print(f'Ip da Rede: {ip1.rede}')
    print(f'Ip de Broadcast: {ip1.broadcast}')
    print(f'Primeiro ip útil: {ip1.primeiro_ip_util}')
    print(f'Ultimo ip útil: {ip1.ultimo_ip_util}')
