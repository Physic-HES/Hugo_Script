function TCP_CloseSocket ( socketId )
%TCP_CloseSocket : Close a socket
%   This function close the bloquing socket opened with XPS.
%   It remains important to call this function, and not leave
%   sockets open when finishing the work with an XPS.

if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return
end

calllib ('XPS_Q8_drivers', 'TCP_CloseSocket', socketId) ;
