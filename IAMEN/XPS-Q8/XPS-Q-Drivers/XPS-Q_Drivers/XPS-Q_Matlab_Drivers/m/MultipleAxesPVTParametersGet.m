function [errorCode, FileName, CurrentElementNumber] = MultipleAxesPVTParametersGet(socketId, GroupName)
%MultipleAxesPVTParametersGet :  Multiple axes PVT trajectory get parameters
%
%	[errorCode, FileName, CurrentElementNumber] = MultipleAxesPVTParametersGet(socketId, GroupName)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%	* Output parameters :
%		int32 errorCode
%		cstring FileName
%		int32Ptr CurrentElementNumber


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
FileName = '';
for i = 1:103
	FileName = [FileName '          '];
end
CurrentElementNumber = 0;

% lib call
[errorCode, GroupName, FileName, CurrentElementNumber] = calllib('XPS_Q8_drivers', 'MultipleAxesPVTParametersGet', socketId, GroupName, FileName, CurrentElementNumber);
