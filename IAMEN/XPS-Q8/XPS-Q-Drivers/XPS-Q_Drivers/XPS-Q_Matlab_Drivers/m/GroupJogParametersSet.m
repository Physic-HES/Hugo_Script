function [errorCode] = GroupJogParametersSet(socketId, GroupName, Velocity, Acceleration)
%GroupJogParametersSet :  Modify Jog parameters on selected group and activate the continuous move
%
%	[errorCode] = GroupJogParametersSet(socketId, GroupName, Velocity, Acceleration)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		double Velocity
%		double Acceleration
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Count the number of element in the API
[tmp, nbElement] = size(Velocity);

% lib call
[errorCode, GroupName] = calllib('XPS_Q8_drivers', 'GroupJogParametersSet', socketId, GroupName, nbElement, Velocity, Acceleration);
